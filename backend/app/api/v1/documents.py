"""文档上传、摄取与管理（列表 / 详情 / 分类 / 删除）。"""
import json
import logging
import uuid
from pathlib import Path

import aiofiles
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import check_ai_quota, get_current_user, get_rag, get_settings
from app.core.config import Settings
from app.core.errors import RAGUnavailableError
from app.db.session import get_db
from app.models import DocumentRecord, User, UserSettings
from app.schemas.document import (
    CategoryCreate,
    CategoryListResponse,
    DocumentCategoryUpdate,
    DocumentListResponse,
    DocumentOut,
    UploadResponse,
)
from app.services.rag.pipeline import RAGPipeline
from app.services.settings_service import (
    get_user_settings,
    resolve_chunk_size,
    resolve_embed,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])

SUPPORTED_EXTENSIONS = {".txt", ".md", ".markdown", ".pdf", ".docx", ".pptx"}


async def _require_db(db_session: AsyncSession | None) -> AsyncSession:
    if db_session is None:
        raise HTTPException(status_code=503, detail="文档管理不可用：数据库未配置")
    return db_session


def _parse_categories(raw: str | None) -> list[str]:
    """解析 user_settings.doc_categories（JSON 数组字符串）；容错返回 []。"""
    if not raw:
        return []
    try:
        items = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return []
    return [c for c in items if isinstance(c, str) and c.strip()]


async def _collect_categories(session: AsyncSession, user_id: int) -> list[str]:
    """并集：user_settings.doc_categories + 用户文档去重分类 + 未分类（去重）。"""
    us = await get_user_settings(session, user_id)
    cats = _parse_categories(us.doc_categories if us else None)
    result = await session.execute(
        select(DocumentRecord.category)
        .distinct()
        .where(DocumentRecord.user_id == user_id)
    )
    for c in result.scalars().all():
        if c and c not in cats:
            cats.append(c)
    if "未分类" not in cats:
        cats.append("未分类")
    return cats


@router.post("/upload", response_model=UploadResponse, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    category: str | None = Form(default=None, description="文档分类，缺省为未分类"),
    current_user: User = Depends(check_ai_quota),
    rag: RAGPipeline = Depends(get_rag),
    settings: Settings = Depends(get_settings),
    db_session: AsyncSession | None = Depends(get_db),
) -> UploadResponse:
    """上传文档并摄取进向量库（multipart 字段名：file、category）。需要登录。"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="缺少文件名")

    ext = Path(file.filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"不支持的格式 {ext or '(无扩展名)'}，支持: {', '.join(sorted(SUPPORTED_EXTENSIONS))}",
        )

    # 落盘留档（上传目录按需创建）
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid.uuid4().hex}_{Path(file.filename).name}"
    dest = settings.upload_dir / stored_name
    try:
        async with aiofiles.open(dest, "wb") as out:
            await out.write(await file.read())
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"保存上传文件失败: {e}") from e

    category = (category or "").strip() or "未分类"  # 归一化：缺省 = 未分类
    us = await get_user_settings(db_session, current_user.id)
    doc_id, chunk_count, db_persisted = await rag.ingest(
        dest,
        file.filename,
        db_session,
        user_id=current_user.id,
        stored_name=stored_name,
        chunk_size=resolve_chunk_size(us, settings),
        category=category,
        embed_overrides=resolve_embed(us, settings),
    )
    return UploadResponse(
        doc_id=doc_id,
        filename=file.filename,
        chunk_count=chunk_count,
        db_persisted=db_persisted,
    )


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    category: str | None = None,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession | None = Depends(get_db),
) -> DocumentListResponse:
    """列出当前用户的文档（按创建时间倒序）；category 非空时按分类过滤。"""
    session = await _require_db(db_session)
    try:
        stmt = (
            select(DocumentRecord)
            .where(DocumentRecord.user_id == current_user.id)
            .order_by(DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
        )
        if category:
            stmt = stmt.where(DocumentRecord.category == category)
        result = await session.execute(stmt)
        rows = result.scalars().all()
    except Exception as e:  # noqa: BLE001
        logger.warning("查询文档列表失败: %s", e)
        raise HTTPException(status_code=503, detail="文档管理不可用：数据库连接失败")

    docs = [DocumentOut.model_validate(r) for r in rows]
    return DocumentListResponse(documents=docs, total=len(docs))


# 注意：/categories 必须在 /{doc_id} 之前声明，否则被路径参数吞掉
@router.get("/categories", response_model=CategoryListResponse)
async def list_categories(
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession | None = Depends(get_db),
) -> CategoryListResponse:
    """列出当前用户全部文档分类（并集），供过滤 pills 与对话「基于」选择器使用。

    DB 不可用时降级返回 ["未分类"]（对话页依赖此接口，不能 503 拖垮对话）。
    """
    if db_session is None:
        return CategoryListResponse(categories=["未分类"])
    try:
        cats = await _collect_categories(db_session, current_user.id)
    except Exception as e:  # noqa: BLE001
        logger.warning("查询文档分类失败（已降级）: %s", e)
        return CategoryListResponse(categories=["未分类"])
    return CategoryListResponse(categories=cats)


@router.post("/categories", response_model=CategoryListResponse, status_code=201)
async def add_category(
    body: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession | None = Depends(get_db),
) -> CategoryListResponse:
    """新建一个文档分类（去重幂等）；「未分类」是内置默认分类不可建。"""
    session = await _require_db(db_session)
    name = body.category.strip()
    if name == "未分类":
        raise HTTPException(status_code=400, detail="「未分类」是内置默认分类，无需新建")
    try:
        us = await get_user_settings(session, current_user.id)
        cats = _parse_categories(us.doc_categories if us else None)
        if name not in cats:
            cats.append(name)
        if us is None:
            us = UserSettings(user_id=current_user.id)
            session.add(us)
        us.doc_categories = json.dumps(cats, ensure_ascii=False)
        await session.commit()
        full = await _collect_categories(session, current_user.id)
    except SQLAlchemyError as e:
        await session.rollback()
        logger.warning("新建文档分类失败: %s", e)
        raise HTTPException(status_code=503, detail="文档管理不可用：数据库连接失败")
    return CategoryListResponse(categories=full)


@router.get("/{doc_id}", response_model=DocumentOut)
async def get_document(
    doc_id: str,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession | None = Depends(get_db),
) -> DocumentOut:
    """查看单个文档详情；非本人文档返回 404。"""
    session = await _require_db(db_session)
    try:
        result = await session.execute(
            select(DocumentRecord).where(
                DocumentRecord.doc_id == doc_id,
                DocumentRecord.user_id == current_user.id,
            )
        )
        record = result.scalar_one_or_none()
    except Exception as e:  # noqa: BLE001
        logger.warning("查询文档详情失败: %s", e)
        raise HTTPException(status_code=503, detail="文档管理不可用：数据库连接失败")
    if record is None:
        raise HTTPException(status_code=404, detail="文档不存在")
    return DocumentOut.model_validate(record)


@router.patch("/{doc_id}", response_model=DocumentOut)
async def update_document_category(
    doc_id: str,
    body: DocumentCategoryUpdate,
    current_user: User = Depends(get_current_user),
    rag: RAGPipeline = Depends(get_rag),
    db_session: AsyncSession | None = Depends(get_db),
) -> DocumentOut:
    """修改文档分类：先更新向量块元数据（Chroma-first），再改 DB。

    PATCH 幂等（重复设置同一分类结果一致），Chroma 已改而 DB 失败时重试可收敛。
    """
    session = await _require_db(db_session)
    try:
        result = await session.execute(
            select(DocumentRecord).where(
                DocumentRecord.doc_id == doc_id,
                DocumentRecord.user_id == current_user.id,
            )
        )
        record = result.scalar_one_or_none()
    except Exception as e:  # noqa: BLE001
        logger.warning("查询文档失败: %s", e)
        raise HTTPException(status_code=503, detail="文档管理不可用：数据库连接失败")
    if record is None:
        raise HTTPException(status_code=404, detail="文档不存在")

    category = body.category.strip()
    try:
        await rag.vectorstore.a_update_doc_category(doc_id, current_user.id, category)
    except RAGUnavailableError as e:
        logger.warning("更新文档向量块分类失败: %s", e)
        raise HTTPException(status_code=503, detail=f"更新失败：{e}") from e

    record.category = category
    try:
        await session.commit()
        await session.refresh(record)
    except Exception as e:  # noqa: BLE001
        await session.rollback()
        logger.warning("更新文档分类记录失败: %s", e)
        raise HTTPException(status_code=503, detail="文档管理不可用：数据库连接失败")
    return DocumentOut.model_validate(record)


@router.delete("/{doc_id}", status_code=204)
async def delete_document(
    doc_id: str,
    current_user: User = Depends(get_current_user),
    rag: RAGPipeline = Depends(get_rag),
    settings: Settings = Depends(get_settings),
    db_session: AsyncSession | None = Depends(get_db),
) -> None:
    """删除本人文档：先删向量块，再删 DB 记录，最后清理磁盘文件。"""
    session = await _require_db(db_session)
    try:
        result = await session.execute(
            select(DocumentRecord).where(
                DocumentRecord.doc_id == doc_id,
                DocumentRecord.user_id == current_user.id,
            )
        )
        record = result.scalar_one_or_none()
    except Exception as e:  # noqa: BLE001
        logger.warning("查询文档失败: %s", e)
        raise HTTPException(status_code=503, detail="文档管理不可用：数据库连接失败")
    if record is None:
        raise HTTPException(status_code=404, detail="文档不存在")

    # 1) 删向量块（失败抛 RAGUnavailableError -> 503，避免留孤儿块）
    try:
        await rag.vectorstore.a_delete_by_doc(doc_id, current_user.id)
    except RAGUnavailableError as e:
        logger.warning("删除文档向量块失败: %s", e)
        raise HTTPException(status_code=503, detail=f"删除失败：{e}") from e

    # 2) 删 DB 记录（笔记无关联，无需级联）
    try:
        await session.delete(record)
        await session.commit()
    except Exception as e:  # noqa: BLE001
        logger.warning("删除文档记录失败: %s", e)
        await session.rollback()
        raise HTTPException(status_code=503, detail="文档管理不可用：数据库连接失败")

    # 3) 清理磁盘文件（尽力而为，失败不影响结果）
    if record.stored_name:
        stored = settings.upload_dir / record.stored_name
        try:
            if stored.is_file():
                stored.unlink()
        except Exception as e:  # noqa: BLE001
            logger.warning("删除磁盘文件失败（忽略）: %s", e)
