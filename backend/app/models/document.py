"""文档元数据表：记录每次摄取到向量库的文档。"""
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DocumentRecord(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    doc_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    filename: Mapped[str] = mapped_column(String(255))
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    # 归属用户；历史数据为 NULL（不可见），新数据必填
    user_id: Mapped[int | None] = mapped_column(Integer, index=True, nullable=True)
    # 上传目录里的存储文件名（uuid 前缀），删除文档时连带清理；历史数据为 NULL
    stored_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # 文档分类（自由字符串），默认「未分类」；对话检索可按分类过滤
    category: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default="未分类", default="未分类"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
