"""日志初始化。"""
import logging
import sys

from app.core.config import Settings


def configure_logging(settings: Settings) -> None:
    """配置根日志：统一格式、输出到 stdout，压低 access 日志噪音。"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        stream=sys.stdout,
        force=True,
    )
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
