"""日志初始化：统一格式 + request_id 注入。"""
import logging
import sys

from app.core.config import Settings
from app.core.context import request_id_var


class ContextFormatter(logging.Formatter):
    """把 ContextVar 里的 request_id 填进 ``%(request_id)s`` 字段。

    非请求上下文（启动、后台任务）默认是 ``-``。asyncio.to_thread 会传播
    ContextVar，因此线程内日志也能带上请求 id。
    """

    def format(self, record: logging.LogRecord) -> str:
        record.request_id = request_id_var.get()
        return super().format(record)


def configure_logging(settings: Settings) -> None:
    """配置根日志：统一格式、输出到 stdout，压低 access 日志噪音。"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | [%(request_id)s] %(message)s",
        stream=sys.stdout,
        force=True,
    )
    for handler in logging.getLogger().handlers:
        handler.setFormatter(ContextFormatter(handler.formatter._fmt or "%(message)s"))
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
