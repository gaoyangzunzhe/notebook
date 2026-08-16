"""ORM 模型聚合导出。

导入本模块会把所有模型注册到 Base.metadata，供 create_all 建表。
"""
from app.models.chat import ChatMessage
from app.models.document import DocumentRecord
from app.models.note import NOTE_TAGS, Note
from app.models.user import User
from app.models.user_settings import UserSettings

__all__ = [
    "ChatMessage",
    "DocumentRecord",
    "Note",
    "NOTE_TAGS",
    "User",
    "UserSettings",
]
