"""AI 调用护栏：全局并发上限（信号量）+ 每用户滑动窗口配额（限流）。

- ``init_guard(settings)`` 由 lifespan 调用（asyncio.Semaphore 需绑定事件循环），
  之后用 ``get_llm_semaphore()`` 取信号量。
- 信号量**不重入**：每个逻辑操作（RAG 提问 / 上传 / 辅助写作 / 自动分类）在入口
  只取一次槽，避免嵌套获取死锁。
- ``SlidingWindowLimiter.hit`` 在事件循环内 check+append 无 await 间隙，天然原子。
"""
import asyncio
import logging
import threading
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from typing import AsyncIterator, Deque

from app.core.config import Settings
from app.core.errors import RateLimitExceeded

logger = logging.getLogger(__name__)

_sem: asyncio.Semaphore | None = None
_limiter: "SlidingWindowLimiter | None" = None
_init_lock = threading.Lock()


def init_guard(settings: Settings) -> None:
    """创建全局信号量与每用户限流器（幂等，lifespan 调用一次即可）。"""
    global _sem, _limiter
    with _init_lock:
        _sem = asyncio.Semaphore(max(1, settings.ai_max_concurrent_llm))
        _limiter = SlidingWindowLimiter(
            settings.ai_quota_limit, settings.ai_quota_window_seconds
        )


def get_llm_semaphore() -> asyncio.Semaphore:
    if _sem is None:
        raise RuntimeError("init_guard(settings) 尚未调用")
    return _sem


@asynccontextmanager
async def llm_slot() -> AsyncIterator[None]:
    """占用一个 LLM/嵌入并发槽。

    信号量不重入：每个逻辑操作（RAG 提问 / 上传 / 辅助写作 / 自动分类）
    在入口只取一次槽，内部嵌套的调用不要再取。
    init_guard 未调用时退化为无限制（幂等降级，不阻塞业务）。
    """
    if _sem is None:
        yield
        return
    async with _sem:
        yield


def check_quota(key: str) -> None:
    """每用户配额检查；超限抛 RateLimitExceeded（0 配额 = 关闭，恒放行）。"""
    if _limiter is not None:
        _limiter.hit(key)


class SlidingWindowLimiter:
    """按 key 的滑动窗口计数限流。

    ``limit <= 0`` 表示关闭（恒放行）。用单调时钟，窗口内命中数 >= limit 即抛
    ``RateLimitExceeded``；线程锁仅防御 to_thread 侧误用，正常只在事件循环调用。
    """

    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = limit
        self.window = window_seconds
        self._buckets: dict[str, Deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def hit(self, key: str) -> None:
        if self.limit <= 0:
            return
        now = time.monotonic()
        cutoff = now - self.window
        with self._lock:
            bucket = self._buckets[key]
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()
            if len(bucket) >= self.limit:
                wait = max(1, int(bucket[0] + self.window - now))
                raise RateLimitExceeded(f"AI 调用过于频繁，请 {wait} 秒后重试")
            bucket.append(now)
