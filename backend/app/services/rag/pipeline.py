"""RAG 流水线编排：摄取（ingest）与问答（ask）。

设计要点：
- 密钥在调用时校验（非启动时），每个 provider 调用都被捕获并转成
  RAGUnavailableError，由 FastAPI 异常处理器输出可读的 503。
- 数据库写入逐个 try/except 守护：DB 不可用时静默降级（db_persisted=False），
  绝不因数据库问题导致请求失败。
"""
import logging
from pathlib import Path
from uuid import uuid4

from langchain_core.documents import Document
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.errors import RAGUnavailableError
from app.models import ChatMessage, DocumentRecord
from app.services.rag.chain import build_retrieval_chain
from app.services.rag.loader import load_document
from app.services.rag.splitter import split_documents
from app.services.rag.vectorstore import VectorStoreManager

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(self, settings: Settings):
        self._settings = settings
        self.vectorstore = VectorStoreManager(settings)

    async def ingest(
        self,
        path: Path,
        filename: str,
        db_session: AsyncSession | None = None,
        user_id: int | None = None,
        stored_name: str | None = None,
        chunk_size: int | None = None,
        category: str | None = None,
        embed_overrides: dict | None = None,
    ) -> tuple[str, int, bool]:
        """摄取文档：加载 -> 切分 -> 向量化 -> 写入 Chroma，并尽力落库元数据。

        返回 (doc_id, chunk_count, db_persisted)。stored_name 是上传目录里的
        存储文件名，用于删除时连带清理磁盘文件。chunk_size 为 None 时用全局值。
        category 为文档分类（默认「未分类」由端点层归一化），写入块元数据与 DB。
        embed_overrides 由端点层按用户级嵌入配置解析后传入。
        """
        doc_id = uuid4().hex
        docs = load_document(path, filename)
        chunks = split_documents(
            docs,
            chunk_size=chunk_size or self._settings.chunk_size,
            chunk_overlap=self._settings.chunk_overlap,
        )
        if not chunks:
            raise RAGUnavailableError("文档内容为空，无法切分")

        chunk_count = self.vectorstore.add_documents(
            chunks,
            user_id=user_id,
            doc_id=doc_id,
            category=category,
            embed_overrides=embed_overrides,
        )
        db_persisted = await self._persist_document(
            db_session, doc_id, filename, chunk_count, user_id, stored_name, category
        )
        logger.info("文档已摄取: %s (%d chunks, %s)", filename, chunk_count, category or "未分类")
        return doc_id, chunk_count, db_persisted

    async def ask(
        self,
        question: str,
        k: int,
        session_id: str | None = None,
        db_session: AsyncSession | None = None,
        user_id: int | None = None,
        category: str | None = None,
        llm_overrides: dict | None = None,
        similarity_threshold: float | None = None,
        embed_overrides: dict | None = None,
    ) -> tuple[str, list[tuple[Document, float]]]:
        """问答：检索 -> 生成。返回 (answer, [(Document, score), ...])。

        category 非空时按知识库分类过滤检索（对话「基于分类」）；None = 全部文档。
        注意 search 与 get_retriever 必须用同一过滤，保证回答与 sources 一致。
        llm_overrides / similarity_threshold / embed_overrides 由端点层按用户设置
        解析后传入，不修改缓存的 RAGPipeline 自身配置。
        """
        scored = self.vectorstore.search(
            question,
            k,
            user_id=user_id,
            category=category,
            min_score=similarity_threshold,
            embed_overrides=embed_overrides,
        )

        retriever = self.vectorstore.get_retriever(
            k, user_id=user_id, category=category, embed_overrides=embed_overrides
        )
        chain = build_retrieval_chain(
            self._settings, retriever, llm_overrides=llm_overrides
        )
        try:
            result = await chain.ainvoke({"input": question})
        except Exception as e:  # noqa: BLE001
            raise RAGUnavailableError(f"对话模型调用失败: {e}") from e

        answer = (result.get("answer") or "").strip()
        if session_id:
            await self._persist_messages(
                db_session, session_id, question, answer, user_id
            )
        return answer, scored

    # ---- 数据库写入（全部守护式）----

    async def _persist_document(
        self,
        session: AsyncSession | None,
        doc_id: str,
        filename: str,
        chunk_count: int,
        user_id: int | None = None,
        stored_name: str | None = None,
        category: str | None = None,
    ) -> bool:
        if session is None:
            return False
        try:
            session.add(
                DocumentRecord(
                    doc_id=doc_id,
                    filename=filename,
                    chunk_count=chunk_count,
                    user_id=user_id,
                    stored_name=stored_name,
                    category=category or "未分类",  # 防御：缺省字段不违反 NOT NULL
                )
            )
            await session.commit()
            return True
        except Exception as e:  # noqa: BLE001
            logger.warning("写入文档元数据失败（已降级）: %s", e)
            await session.rollback()
            return False

    async def _persist_messages(
        self,
        session: AsyncSession | None,
        session_id: str,
        question: str,
        answer: str,
        user_id: int | None = None,
    ) -> None:
        if session is None:
            return
        try:
            session.add_all(
                [
                    ChatMessage(
                        session_id=session_id,
                        role="user",
                        content=question,
                        user_id=user_id,
                    ),
                    ChatMessage(
                        session_id=session_id,
                        role="assistant",
                        content=answer,
                        user_id=user_id,
                    ),
                ]
            )
            await session.commit()
        except Exception as e:  # noqa: BLE001
            logger.warning("写入聊天记录失败（已降级）: %s", e)
            await session.rollback()
