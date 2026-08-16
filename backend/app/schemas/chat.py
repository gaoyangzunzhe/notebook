"""聊天历史响应模型。"""
from datetime import datetime

from pydantic import BaseModel


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    session_id: str
    db_available: bool
    messages: list[MessageOut]


class SessionSummary(BaseModel):
    """会话列表条目：标题取首条用户消息（≤30 字），兜底「新对话」。"""

    session_id: str
    title: str
    last_message: str
    message_count: int
    updated_at: datetime


class ChatSessionsResponse(BaseModel):
    sessions: list[SessionSummary]
    total: int
    db_available: bool = True
