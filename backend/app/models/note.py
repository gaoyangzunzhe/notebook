"""笔记模型：用户自己写的内容，独立存在，不绑定笔记本。

AI 辅助写作只基于笔记正文；知识库文档仅通过编辑器右侧「相关文档」推荐面板
间接出现（临时 RAG 检索，不持久化关联）。
"""
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

# 笔记分类固定取值：分类 prompt 与入参校验共用，保持单一来源
NOTE_TAGS: tuple[str, ...] = ("工作", "学习", "生活", "技术", "其他")


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)  # 归属用户
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text, default="")
    # 笔记分类（NOTE_TAGS 之一）：AI 自动建议 + 编辑器手动修改
    tag: Mapped[str | None] = mapped_column(String(16), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
