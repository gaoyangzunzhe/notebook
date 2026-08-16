"""异步引擎与会话管理。

设计目标：懒连接。init_engine() 只创建 engine（不会真正连接数据库，
create_async_engine 在首次使用时才连），因此 Postgres 没启动应用也能跑。
"""
import logging
from typing import Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import Settings

logger = logging.getLogger(__name__)

_engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


def init_engine(settings: Settings) -> None:
    """按配置创建异步引擎；DATABASE_URL 为空则保持 None（DB 未配置）。"""
    global _engine, _session_factory
    if not settings.database_url:
        logger.info("DATABASE_URL 未配置，数据库功能停用。")
        _engine = None
        _session_factory = None
        return
    _engine = create_async_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_size=5,
        echo=False,
    )
    _session_factory = async_sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)


def get_engine() -> Optional[AsyncEngine]:
    return _engine


def get_session_factory() -> Optional[async_sessionmaker[AsyncSession]]:
    return _session_factory


async def dispose_engine() -> None:
    """关闭引擎；未初始化时静默跳过。"""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None


async def get_db() -> Optional[AsyncSession]:
    """FastAPI 依赖：产出会话；DB 不可用时产出 None（由调用方自行兜底）。"""
    factory = _session_factory
    if factory is None:
        yield None
        return
    async with factory() as session:
        yield session
