"""FastAPI 依赖与组件状态探测。

RAGPipeline 采用懒构建：首次请求时才创建，并缓存到 app.state.rag。
这样启动阶段不会连接 Chroma / 调用任何外部服务，保证快速且健壮。
"""
import asyncio
import logging

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import Settings
from app.core.guard import check_quota
from app.core.security import decode_access_token
from app.db import session as db_session
from app.db.session import get_db
from app.models import User
from app.services.rag.pipeline import RAGPipeline

logger = logging.getLogger(__name__)

# auto_error=False：缺/坏 Authorization 头时由我们自己转 401（FastAPI 默认会转 403）
_bearer = HTTPBearer(auto_error=False)


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_rag(request: Request) -> RAGPipeline:
    rag = request.app.state.rag
    if rag is None:
        rag = RAGPipeline(request.app.state.settings)
        request.app.state.rag = rag
    return rag


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    settings: Settings = Depends(get_settings),
    db_session: AsyncSession | None = Depends(get_db),
) -> User:
    """校验 Bearer token 并从数据库加载当前用户。

    401 统一带 WWW-Authenticate: Bearer；DB 不可用时 503 快速失败。
    """
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="未登录",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_access_token(credentials.credentials, settings)
        user_id = int(payload["sub"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="登录已过期，请重新登录",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="无效的凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if db_session is None:
        raise HTTPException(status_code=503, detail="认证服务不可用：数据库未配置")
    try:
        async with asyncio.timeout(5):
            result = await db_session.execute(select(User).where(User.id == user_id))
    except Exception as e:  # noqa: BLE001
        logger.warning("get_current_user 查询用户失败：%s", e)
        raise HTTPException(status_code=503, detail="认证服务不可用：数据库连接失败")

    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="用户不存在或已被删除",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def check_ai_quota(
    current_user: User = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
) -> User:
    """每用户 AI 调用配额依赖（滑动窗口）。

    只有花钱/耗资源端点挂它；``ai_quota_limit <= 0`` 表示关闭（恒放行）。
    超限抛 RateLimitExceeded -> 429（FastAPI 缓存依赖，get_current_user 不会重复执行）。
    """
    if settings.ai_quota_limit > 0:
        check_quota(f"user:{current_user.id}")
    return current_user


# ---- 组件状态探测（供健康检查展示，只做轻量探测，不硬失败）----

async def db_status(settings: Settings) -> str:
    engine = db_session.get_engine()
    if engine is None:
        return "not-configured"
    try:
        async with asyncio.timeout(2):
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        return "up"
    except Exception as e:  # noqa: BLE001
        logger.debug("db probe failed: %s", e)
        return "down"


def vectorstore_status(settings: Settings) -> str:
    try:
        client = chromadb.PersistentClient(
            path=str(settings.chroma_dir),
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        client.list_collections()
        return "up"
    except Exception as e:  # noqa: BLE001
        logger.debug("vectorstore probe failed: %s", e)
        return "down"


def llm_status(settings: Settings) -> str:
    if settings.llm_api_key and settings.llm_base_url:
        return "configured"
    return "not-configured"
