"""聊天历史（按会话查询）。DB 不可用时返回空列表 + db_available=false。"""
import logging

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import ChatMessage, User
from app.schemas.chat import (
    ChatHistoryResponse,
    ChatSessionsResponse,
    MessageOut,
    SessionSummary,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/sessions", response_model=ChatSessionsResponse)
async def list_sessions(
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession | None = Depends(get_db),
) -> ChatSessionsResponse:
    """列出当前用户的会话列表。

    单次按 (session_id, id) 升序取全量，在 Python 内聚合（升序 id 保证首条
    user 消息即标题、末行即最近更新）。会话量级为单用户聊天历史，规模不大；
    若表增长可改用 SQL DISTINCT ON (session_id) 各会话取 count + 最近一条。
    """
    if db_session is None:
        return ChatSessionsResponse(sessions=[], total=0, db_available=False)
    try:
        result = await db_session.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == current_user.id)
            .order_by(ChatMessage.session_id, ChatMessage.id)
        )
        rows = result.scalars().all()
    except Exception as e:  # noqa: BLE001
        logger.warning("查询会话列表失败（已降级）: %s", e)
        return ChatSessionsResponse(sessions=[], total=0, db_available=False)

    agg: dict[str, dict] = {}
    for m in rows:
        s = agg.setdefault(
            m.session_id,
            {
                "session_id": m.session_id,
                "message_count": 0,
                "updated_at": m.created_at,
                "last_message": m.content,
                "title_user": "",
            },
        )
        s["message_count"] += 1
        if m.role == "user" and not s["title_user"]:
            s["title_user"] = m.content
        s["updated_at"] = m.created_at  # id 升序 ⇒ 末行即最近
        s["last_message"] = m.content

    sessions = [
        SessionSummary(
            session_id=s["session_id"],
            title=(s["title_user"] or "新对话").replace("\n", " ")[:30],
            last_message=s["last_message"],
            message_count=s["message_count"],
            updated_at=s["updated_at"],
        )
        for s in sorted(agg.values(), key=lambda s: s["updated_at"], reverse=True)
    ]
    return ChatSessionsResponse(sessions=sessions, total=len(sessions))


@router.get("/sessions/{session_id}/messages", response_model=ChatHistoryResponse)
async def list_messages(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession | None = Depends(get_db),
) -> ChatHistoryResponse:
    if db_session is None:
        return ChatHistoryResponse(session_id=session_id, db_available=False, messages=[])
    try:
        result = await db_session.execute(
            select(ChatMessage)
            .where(
                ChatMessage.session_id == session_id,
                ChatMessage.user_id == current_user.id,
            )
            .order_by(ChatMessage.id)
        )
        rows = result.scalars().all()
        messages = [
            MessageOut(id=m.id, role=m.role, content=m.content, created_at=m.created_at)
            for m in rows
        ]
        return ChatHistoryResponse(session_id=session_id, db_available=True, messages=messages)
    except Exception as e:  # noqa: BLE001
        logger.warning("查询聊天记录失败（已降级）: %s", e)
        return ChatHistoryResponse(session_id=session_id, db_available=False, messages=[])
