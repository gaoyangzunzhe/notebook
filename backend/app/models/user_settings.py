"""用户级配置表：覆盖全局 .env 默认值（user_settings，一行/用户）。

- LLM：provider/model/api_key(加密)/temperature
- 嵌入模型：embed_provider/embed_model/embed_api_key(加密)
- RAG：top_k / chunk_size / similarity_threshold
- UI：theme / sidebar_collapsed（localStorage 为主，登录后同步到此处）

各字段 nullable，NULL = 继承全局 .env 默认。
"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)

    # ---- LLM（provider 为 NULL 时继承 .env）----
    llm_provider: Mapped[str | None] = mapped_column(String(32), nullable=True)
    llm_model: Mapped[str | None] = mapped_column(String(64), nullable=True)
    llm_base_url: Mapped[str | None] = mapped_column(
        String(256), nullable=True
    )  # 自定义接口地址（网关/代理），覆盖提供商注册表默认
    llm_api_key_encrypted: Mapped[str | None] = mapped_column(String(512), nullable=True)
    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0.0–2.0

    # ---- 嵌入模型（provider 为 NULL 时继承 .env）----
    embed_provider: Mapped[str | None] = mapped_column(String(32), nullable=True)
    embed_model: Mapped[str | None] = mapped_column(String(64), nullable=True)
    embed_base_url: Mapped[str | None] = mapped_column(
        String(256), nullable=True
    )  # 自定义接口地址（网关/代理），覆盖提供商注册表默认
    embed_api_key_encrypted: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # ---- RAG ----
    top_k: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 1–20
    chunk_size: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 200–8000
    similarity_threshold: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0.0–1.0

    # ---- 知识库分类清单（JSON 数组字符串，用户自建分类；过滤 pills 用）----
    doc_categories: Mapped[str | None] = mapped_column(Text, nullable=True, default="[]")

    # ---- UI 偏好（localStorage 为主，此处为登录后同步副本）----
    theme: Mapped[str | None] = mapped_column(String(16), nullable=True)  # light|dark|system
    sidebar_collapsed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
