"""向量库封装：Chroma 持久化。

VectorStoreManager 是向量库的"单点隔离"——后续若迁移到 Chroma HTTP/Cloud 版，
只需改动本类，上层 pipeline / 路由无需感知。

同步方法（add_documents 等）都是阻塞 I/O，会卡住事件循环：
调用方一律走 ``a_*`` 异步包装（asyncio.to_thread 卸载到线程池）。
"""
import asyncio
import logging
import time

import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core import metrics
from app.core.config import Settings
from app.core.errors import RAGConfigurationError, RAGUnavailableError
from app.services.rag.embeddings import get_embeddings

logger = logging.getLogger(__name__)

COLLECTION_NAME = "notebook_docs"


class VectorStoreManager:
    def __init__(self, settings: Settings):
        self._settings = settings
        settings.chroma_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=str(settings.chroma_dir),  # 必须绝对路径（Windows 上相对路径不可靠）
            settings=ChromaSettings(anonymized_telemetry=False),
        )

    def _get_store(self, embed_overrides: dict | None = None) -> Chroma:
        """加载既有集合（不重复建/写），用于检索。"""
        return Chroma(
            client=self.client,
            collection_name=COLLECTION_NAME,
            embedding_function=get_embeddings(
                self._settings, overrides=embed_overrides
            ),
        )

    def add_documents(
        self,
        docs: list[Document],
        user_id: int | None = None,
        doc_id: str | None = None,
        category: str | None = None,
        embed_overrides: dict | None = None,
    ) -> int:
        """写入文档块到集合，返回写入的块数。

        多租户隔离：给每个块注入归属用户的 user_id 元数据
        （单集合 + 元数据过滤方案），检索时按 user_id 过滤；
        doc_id 用于「按文档删除」，category 用于对话按知识库分类过滤，
        一并写入块元数据。category 为 None 时不写入（旧调用方不破，
        且「未分类」过滤依赖写入时的 category='未分类'）。
        embed_overrides 由端点层按用户级嵌入配置解析后传入。
        """
        if not docs:
            return 0
        owned: list[Document] = []
        for doc in docs:
            metadata = dict(doc.metadata)
            if user_id is not None:
                metadata["user_id"] = user_id
            if doc_id is not None:
                metadata["doc_id"] = doc_id
            if category is not None:
                metadata["category"] = category
            owned.append(Document(page_content=doc.page_content, metadata=metadata))
        try:
            Chroma.from_documents(
                documents=owned,
                embedding=get_embeddings(
                    self._settings, overrides=embed_overrides
                ),
                client=self.client,
                collection_name=COLLECTION_NAME,
            )
        except RAGConfigurationError:
            raise
        except Exception as e:  # noqa: BLE001
            raise RAGUnavailableError(f"向量库写入失败: {e}") from e
        return len(owned)

    def _user_filter(self, user_id: int | None) -> dict | None:
        """按 user_id 构造 Chroma where 过滤；user_id 为空时不过滤（保持旧行为）。"""
        if user_id is None:
            return None
        return {"user_id": user_id}

    def _combined_filter(
        self,
        user_id: int | None,
        category: str | None = None,
    ) -> dict | None:
        """组合 Chroma where 过滤：user_id 等值 + 可选 category 等值（$and 连接）。"""
        filt = self._user_filter(user_id)
        if category:
            cat_filter = {"category": category}
            filt = {"$and": [filt, cat_filter]} if filt is not None else cat_filter
        return filt

    def search(
        self,
        query: str,
        k: int,
        user_id: int | None = None,
        category: str | None = None,
        min_score: float | None = None,
        embed_overrides: dict | None = None,
    ) -> list[tuple[Document, float]]:
        """按语义相似度检索，返回 (Document, 相关度分数) 列表。

        category 非空时在 user_id 过滤之上加分类等值过滤（对话「基于分类」检索）。
        min_score 非空时只保留相关度 >= 阈值的块（用户级相似度阈值）。
        embed_overrides 由端点层按用户级嵌入配置解析后传入。
        """
        try:
            store = self._get_store(embed_overrides)
            kwargs: dict = {"k": k}
            filt = self._combined_filter(user_id, category)
            if filt is not None:
                kwargs["filter"] = filt
            results = store.similarity_search_with_relevance_scores(query, **kwargs)
            if min_score is not None:
                results = [(doc, score) for doc, score in results if score >= min_score]
            return results
        except RAGConfigurationError:
            raise
        except Exception as e:  # noqa: BLE001
            raise RAGUnavailableError(f"向量检索失败: {e}") from e

    def get_retriever(
        self,
        k: int,
        user_id: int | None = None,
        category: str | None = None,
        embed_overrides: dict | None = None,
    ):
        """构建 LangChain retriever，供 RAG 链使用。

        注意：category 过滤必须与 search 一致，否则回答内容与 sources 不一致
        （LLM 会取到未过滤的文档块）。
        """
        kwargs: dict = {"k": k}
        filt = self._combined_filter(user_id, category)
        if filt is not None:
            kwargs["filter"] = filt
        return self._get_store(embed_overrides).as_retriever(search_kwargs=kwargs)

    def delete_by_doc(self, doc_id: str, user_id: int) -> int:
        """删除某用户某文档的向量块，返回删除条数。

        按 (user_id, doc_id) 两个条件过滤，保证只删本人文档的块。
        失败抛 RAGUnavailableError（由调用方转 503），避免 DB 记录已删、
        向量块成孤儿的脏状态。
        """
        try:
            col = self.client.get_collection(COLLECTION_NAME)
        except Exception:  # noqa: BLE001
            # 集合不存在 = 没有可删的块
            return 0
        try:
            deleted = col.delete(
                where={"$and": [{"user_id": user_id}, {"doc_id": doc_id}]}
            )
            return len(deleted) if isinstance(deleted, list) else 0
        except RAGConfigurationError:
            raise
        except Exception as e:  # noqa: BLE001
            raise RAGUnavailableError(f"删除向量块失败: {e}") from e

    def update_doc_category(self, doc_id: str, user_id: int, category: str) -> int:
        """更新某用户某文档全部向量块的 category 元数据，返回更新条数。

        Chroma-first：先改向量块，再改 DB，重试可幂等收敛（改分类的 PATCH
        幂等——重复设置同一分类结果一致）。
        """
        try:
            col = self.client.get_collection(COLLECTION_NAME)
        except Exception:  # noqa: BLE001
            # 集合不存在 = 没有可改的块
            return 0
        try:
            got = col.get(
                where={"$and": [{"user_id": user_id}, {"doc_id": doc_id}]},
                include=["metadatas"],
            )
            ids = got.get("ids") or []
            if not ids:
                return 0
            metas = [dict(m, category=category) for m in (got.get("metadatas") or [])]
            col.update(ids=ids, metadatas=metas)
            return len(ids)
        except RAGConfigurationError:
            raise
        except Exception as e:  # noqa: BLE001
            raise RAGUnavailableError(f"更新向量块分类失败: {e}") from e

    # ---- 异步包装：Chroma 是同步阻塞 I/O，全部丢线程池，避免卡死事件循环 ----

    async def a_add_documents(self, *args, **kwargs) -> int:
        start = time.monotonic()
        try:
            result = await asyncio.to_thread(self.add_documents, *args, **kwargs)
        except RAGConfigurationError:
            metrics.record_embed((time.monotonic() - start) * 1000, error=True)
            raise
        except Exception:
            metrics.record_embed((time.monotonic() - start) * 1000, error=True)
            raise
        metrics.record_embed((time.monotonic() - start) * 1000)
        return result

    async def a_search(self, *args, **kwargs) -> list[tuple[Document, float]]:
        return await asyncio.to_thread(self.search, *args, **kwargs)

    async def a_update_doc_category(self, *args, **kwargs) -> int:
        return await asyncio.to_thread(self.update_doc_category, *args, **kwargs)

    async def a_delete_by_doc(self, *args, **kwargs) -> int:
        return await asyncio.to_thread(self.delete_by_doc, *args, **kwargs)
