"""纯 ASGI 请求上下文中间件：request_id + X-Request-Id + 请求日志/指标。

不用 ``BaseHTTPMiddleware``：它会缓冲 body 并破坏 SSE 流式输出，
这里直接实现 ``__call__`` 纯 ASGI 层，完全不触碰 body。
"""
import logging
import time
import uuid

from app.core import metrics
from app.core.context import request_id_var

logger = logging.getLogger(__name__)


class RequestContextMiddleware:
    """生成 request_id 写入 ContextVar（可传播进 to_thread 线程日志）、
    注入 ``X-Request-Id`` 响应头，完成后记一行 INFO 请求日志并计入 metrics。"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = uuid.uuid4().hex[:12]
        token = request_id_var.set(request_id)
        start = time.monotonic()
        status = {"code": 0}

        async def send_with_header(message):
            if message["type"] == "http.response.start":
                status["code"] = message["status"]
                headers = list(message.get("headers") or [])
                headers.append((b"x-request-id", request_id.encode("ascii")))
                message = dict(message, headers=headers)
            await send(message)

        try:
            await self.app(scope, receive, send_with_header)
        finally:
            ms = (time.monotonic() - start) * 1000
            logger.info(
                "request %s %s -> %s (%.0fms)",
                scope.get("method", ""),
                scope.get("path", ""),
                status["code"],
                ms,
            )
            metrics.record_request(scope.get("path", ""), status["code"], ms)
            request_id_var.reset(token)
