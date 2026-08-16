"""Redis 缓存（可选）。

配置 ``REDIS_URL`` 后启用（当前用于提供商模型列表缓存）；未配置、连不上或
任意一次读写失败时**自动降级为禁用**（返回 None / 静默忽略），业务功能不受影响。

降级带 30s 冷却：Redis 挂了不会每个请求都吃一次连接超时。
"""
import logging
import time
from typing import Optional

import redis.asyncio as aioredis

from app.core.config import Settings

logger = logging.getLogger(__name__)

# Redis 连接超时（秒）：不可达时快速失败，避免请求被拖住
_CONNECT_TIMEOUT = 1.0
_DEGRADE_COOLDOWN = 30.0  # 一次失败后跳过 Redis 的时间（秒）

_client: Optional[aioredis.Redis] = None
_client_url: str = ""
_degraded_until: float = 0.0


def _is_degraded() -> bool:
    return time.monotonic() < _degraded_until


def _mark_degraded() -> None:
    global _degraded_until
    _degraded_until = time.monotonic() + _DEGRADE_COOLDOWN


def get_redis(settings: Settings) -> Optional[aioredis.Redis]:
    """惰性创建 Redis 客户端；未配置 URL 或创建失败返回 None（缓存禁用）。"""
    global _client, _client_url
    if not settings.redis_url:
        return None
    if _is_degraded():
        return None
    if _client is not None and _client_url == settings.redis_url:
        return _client
    try:
        _client = aioredis.from_url(
            settings.redis_url,
            decode_responses=True,
            socket_connect_timeout=_CONNECT_TIMEOUT,
            socket_timeout=_CONNECT_TIMEOUT,
        )
        _client_url = settings.redis_url
        return _client
    except Exception as e:  # noqa: BLE001
        logger.warning("Redis 客户端创建失败，缓存降级为禁用：%s", e)
        _client = None
        _mark_degraded()
        return None


async def cache_get(settings: Settings, key: str) -> Optional[str]:
    """读缓存；任何失败（未配置/连不上/超时）返回 None，不影响业务。"""
    client = get_redis(settings)
    if client is None:
        return None
    try:
        return await client.get(key)
    except Exception as e:  # noqa: BLE001
        logger.debug("Redis GET %s 失败，降级：%s", key, e)
        _mark_degraded()
        return None


async def cache_set(settings: Settings, key: str, value: str, ttl: int) -> None:
    """写缓存（带 TTL）；任何失败静默忽略。"""
    client = get_redis(settings)
    if client is None:
        return
    try:
        await client.set(key, value, ex=ttl)
    except Exception as e:  # noqa: BLE001
        logger.debug("Redis SET %s 失败，忽略：%s", key, e)
        _mark_degraded()
