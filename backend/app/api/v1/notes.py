"""笔记列表 / 详情 / 更新 / 删除、AI 写作辅助（SSE）、分类与「相关文档」推荐。

assist 端点契约：所有可「快速失败」的步骤（鉴权、LLM 配置、提示词构造）都在
返回 StreamingResponse 之前完成，错误以正常 HTTP 状态码返回；响应开始后仅
LLM token 生成，中途失败转为 SSE error 事件。

AI 辅助写作只基于笔记正文（不检索知识库），保证低延迟；知识库文档仅通过
「相关文档」推荐端点间接出现（临时检索，不持久化关联）。
"""
import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import check_ai_quota, get_current_user, get_rag, get_settings
from app.core.config import Settings
from app.db.session import get_db
from app.models import DocumentRecord, Note, User
from app.schemas.note import (
    AssistAction,
    AssistRequest,
    NoteCreate,
    NoteListResponse,
    NoteOut,
    NoteUpdate,
    RelatedDocumentListResponse,
    RelatedDocumentOut,
    TagResponse,
)
from app.services.ai.tagging import classify_tag
from app.services.ai.writing import (
    build_messages,
    stream_assist,
    tail_truncate,
)
from app.services.rag.chain import get_llm
from app.services.rag.pipeline import RAGPipeline
from app.services.settings_service import (
    get_user_settings,
    resolve_embed,
    resolve_llm,
    resolve_threshold,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notes", tags=["notes"])

SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
}


async def _require_db(db_session: AsyncSession | None) -> AsyncSession:
    if db_session is None:
        raise HTTPException(status_code=503, detail="笔记功能不可用：数据库未配置")
    return db_session


async def _get_owned_note(session: AsyncSession, note_id: int, user_id: int) -> Note:
    """按 (id, user_id) 取笔记；不存在或非本人 -> 404（不泄露存在性）。"""
    try:
        result = await session.execute(
            select(Note).where(Note.id == note_id, Note.user_id == user_id)
        )
        note = result.scalar_one_or_none()
    except SQLAlchemyError as e:
        logger.warning("查询笔记失败: %s", e)
        raise HTTPException(status_code=503, detail="笔记功能不可用：数据库连接失败") from e
    if note is None:
        raise HTTPException(status_code=404, detail="笔记不存在")
    return note


@router.get("", response_model=NoteListResponse)
async def list_notes(
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession | None = Depends(get_db),
) -> NoteListResponse:
    """列出当前用户全部笔记（最近更新在前）。"""
    session = await _require_db(db_session)
    try:
        result = await session.execute(
            select(Note)
            .where(Note.user_id == current_user.id)
            .order_by(Note.updated_at.desc(), Note.id.desc())
        )
        notes = result.scalars().all()
    except SQLAlchemyError as e:
        logger.warning("查询笔记列表失败: %s", e)
        raise HTTPException(status_code=503, detail="笔记功能不可用：数据库连接失败") from e
    return NoteListResponse(
        notes=[NoteOut.model_validate(n) for n in notes], total=len(notes)
    )


@router.post("", response_model=NoteOut, status_code=201)
async def create_note(
    body: NoteCreate,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession | None = Depends(get_db),
) -> NoteOut:
    """新建自由笔记（不绑定笔记本，也无需选分类）。"""
    session = await _require_db(db_session)
    note = Note(user_id=current_user.id, title=body.title, content=body.content)
    try:
        session.add(note)
        await session.commit()
        await session.refresh(note)
    except SQLAlchemyError as e:
        await session.rollback()
        logger.warning("创建笔记失败: %s", e)
        raise HTTPException(status_code=503, detail="笔记功能不可用：数据库连接失败") from e
    return NoteOut.model_validate(note)


@router.get("/{note_id}", response_model=NoteOut)
async def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession | None = Depends(get_db),
) -> NoteOut:
    """查看笔记详情。"""
    session = await _require_db(db_session)
    note = await _get_owned_note(session, note_id, current_user.id)
    return NoteOut.model_validate(note)


@router.patch("/{note_id}", response_model=NoteOut)
async def update_note(
    note_id: int,
    body: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession | None = Depends(get_db),
) -> NoteOut:
    """更新笔记（标题 / 内容 / 分类；tag 必须为固定五类之一）。"""
    session = await _require_db(db_session)
    note = await _get_owned_note(session, note_id, current_user.id)
    if body.title is not None:
        note.title = body.title
    if body.content is not None:
        note.content = body.content
    if body.tag is not None:
        note.tag = body.tag
    try:
        await session.commit()
        await session.refresh(note)
    except SQLAlchemyError as e:
        await session.rollback()
        logger.warning("更新笔记失败: %s", e)
        raise HTTPException(status_code=503, detail="笔记功能不可用：数据库连接失败") from e
    return NoteOut.model_validate(note)


@router.delete("/{note_id}", status_code=204)
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession | None = Depends(get_db),
) -> None:
    """删除笔记（内容独立，无需清理向量库）。"""
    session = await _require_db(db_session)
    note = await _get_owned_note(session, note_id, current_user.id)
    try:
        await session.delete(note)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        logger.warning("删除笔记失败: %s", e)
        raise HTTPException(status_code=503, detail="笔记功能不可用：数据库连接失败") from e


@router.get("/{note_id}/related-documents", response_model=RelatedDocumentListResponse)
async def related_documents(
    note_id: int,
    current_user: User = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
    rag: RAGPipeline = Depends(get_rag),
    db_session: AsyncSession | None = Depends(get_db),
) -> RelatedDocumentListResponse:
    """「相关文档」推荐：用笔记正文对知识库做临时检索，不持久化关联。

    按 doc_id 去重（取每文档最高分块）；filename 优先从 DB 补全，DB 不可用时
    回退向量块 metadata 的 source。仅作参考展示，无任何硬关联。
    """
    session = await _require_db(db_session)
    note = await _get_owned_note(session, note_id, current_user.id)
    us = await get_user_settings(db_session, current_user.id)

    query = (note.content or "").strip() or note.title
    if not query:
        return RelatedDocumentListResponse(related=[])

    scored = await rag.vectorstore.a_search(
        query,
        k=5,
        user_id=current_user.id,
        min_score=resolve_threshold(us, settings),
        embed_overrides=resolve_embed(us, settings),
    )

    # 一次查询补齐 (doc_id -> filename, chunk_count)
    db_meta: dict[str, tuple[str, int]] = {}
    if db_session is not None:
        try:
            result = await session.execute(
                select(
                    DocumentRecord.filename,
                    DocumentRecord.doc_id,
                    DocumentRecord.chunk_count,
                ).where(DocumentRecord.user_id == current_user.id)
            )
            db_meta = {
                doc_id: (filename, chunk_count)
                for filename, doc_id, chunk_count in result.all()
            }
        except SQLAlchemyError as e:
            logger.warning("查询文档元数据失败（已降级）: %s", e)

    related: list[RelatedDocumentOut] = []
    seen: set[str] = set()
    for doc, score in scored:
        doc_id = doc.metadata.get("doc_id")
        if not doc_id or doc_id in seen:
            continue
        seen.add(doc_id)
        filename, chunk_count = db_meta.get(doc_id, (None, 0))
        if not filename:
            filename = doc.metadata.get("source") or doc_id
        related.append(
            RelatedDocumentOut(
                doc_id=doc_id,
                filename=filename,
                score=round(score, 4),
                chunk_count=chunk_count,
            )
        )
    return RelatedDocumentListResponse(related=related)


@router.post("/{note_id}/assist")
async def note_assist(
    note_id: int,
    body: AssistRequest,
    current_user: User = Depends(check_ai_quota),
    settings: Settings = Depends(get_settings),
    db_session: AsyncSession | None = Depends(get_db),
) -> StreamingResponse:
    """续写 / 扩写 / 改写，SSE 流式返回。

    只基于笔记正文（+选中文本 +指令），不检索知识库，保证低延迟。
    流开始前完成全部预检（鉴权、LLM 配置、提示词构造），失败以正常 HTTP
    状态码返回；流开始后中途失败发 SSE error 事件收尾。
    """
    session = await _require_db(db_session)
    note = await _get_owned_note(session, note_id, current_user.id)
    us = await get_user_settings(db_session, current_user.id)

    # 1) LLM 配置预检：api_key 缺失 -> RAGConfigurationError -> 400（流未开始）
    llm = get_llm(settings, overrides=resolve_llm(us, settings))

    # 2) 构造提示词（续写取光标前末尾内容，贴近当前上下文）
    cursor = len(note.content)
    if body.action is AssistAction.continue_writing and body.cursor_position is not None:
        cursor = min(body.cursor_position, len(note.content))
    content_prefix = tail_truncate(
        note.content[:cursor], settings.assist_max_note_chars
    )
    messages = build_messages(
        body.action.value,
        title=note.title,
        content_prefix=content_prefix,
        selected_text=body.selected_text or "",
        instruction=body.instruction or "",
    )

    # 3) 返回 SSE 流
    return StreamingResponse(
        stream_assist(llm, messages, timeout_seconds=settings.assist_timeout_seconds),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )


@router.post("/{note_id}/tags", response_model=TagResponse)
async def note_tag(
    note_id: int,
    current_user: User = Depends(check_ai_quota),
    settings: Settings = Depends(get_settings),
    db_session: AsyncSession | None = Depends(get_db),
) -> TagResponse:
    """用 LLM 把笔记归入固定五类分类（AI 建议）并持久化（保存后前端调用）。

    DB 写失败降级：仍返回分类结果（沿用 pipeline「DB 写入守护」惯例）。
    """
    session = await _require_db(db_session)
    note = await _get_owned_note(session, note_id, current_user.id)
    us = await get_user_settings(db_session, current_user.id)
    tag = await classify_tag(
        settings,
        note.title,
        note.content,
        llm=get_llm(settings, overrides=resolve_llm(us, settings)),
    )
    try:
        note.tag = tag
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        logger.warning("写入笔记分类失败（已降级，仍返回分类结果）: %s", e)
    return TagResponse(tag=tag)
