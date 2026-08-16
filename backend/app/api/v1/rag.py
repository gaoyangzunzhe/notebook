"""RAG 问答。"""
from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import check_ai_quota, get_current_user, get_rag, get_settings
from app.core.config import Settings
from app.db.session import get_db
from app.models import User
from app.schemas.rag import QueryRequest, QueryResponse, SourceChunk
from app.services.rag.pipeline import RAGPipeline
from app.services.settings_service import (
    get_user_settings,
    resolve_embed,
    resolve_llm,
    resolve_threshold,
    resolve_top_k,
)

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/query", response_model=QueryResponse)
async def rag_query(
    body: QueryRequest,
    current_user: User = Depends(check_ai_quota),
    rag: RAGPipeline = Depends(get_rag),
    settings: Settings = Depends(get_settings),
    db_session: AsyncSession | None = Depends(get_db),
) -> QueryResponse:
    """基于知识库回答用户问题。缺省 session_id 时后端自动生成。需要登录。

    k / LLM 配置 / 相似度阈值均按 user_settings 覆盖 .env 后生效。
    """
    us = await get_user_settings(db_session, current_user.id)
    session_id = body.session_id or f"s-{uuid4().hex[:8]}"
    answer, scored = await rag.ask(
        question=body.question,
        k=resolve_top_k(body.k, us, settings),
        session_id=session_id,
        db_session=db_session,
        user_id=current_user.id,
        llm_overrides=resolve_llm(us, settings),
        similarity_threshold=resolve_threshold(us, settings),
        embed_overrides=resolve_embed(us, settings),
        category=body.category,
    )
    sources = [
        SourceChunk(
            text=doc.page_content,
            source=doc.metadata.get("source", "unknown"),
            score=round(score, 4),
        )
        for doc, score in scored
    ]
    return QueryResponse(answer=answer, session_id=session_id, sources=sources)
