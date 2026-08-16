"""FastAPI 应用工厂与入口。"""
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import Settings
from app.core.errors import (
    RAGConfigurationError,
    RAGUnavailableError,
    RateLimitExceeded,
    rag_config_error_handler,
    rag_unavailable_error_handler,
    rate_limit_error_handler,
)
from app.core.guard import init_guard
from app.core.logging import configure_logging
from app.core.middleware import RequestContextMiddleware
from app.db import session as db_session
from app.db.init_db import init_db

logger = logging.getLogger(__name__)

# 默认线程池有界化：防止 asyncio.to_thread 在突发时无限建线程
_DEFAULT_EXECUTOR_WORKERS = 8


def create_app() -> FastAPI:
    settings = Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        configure_logging(settings)
        settings.apply_runtime_env()
        app.state.settings = settings
        app.state.rag = None

        # 护栏（信号量 + 每用户限流）需绑定事件循环，必须由 lifespan 创建
        init_guard(settings)
        loop = asyncio.get_running_loop()
        loop.set_default_executor(
            ThreadPoolExecutor(max_workers=_DEFAULT_EXECUTOR_WORKERS)
        )

        # 懒连接：create_engine 不连接；建表失败只告警，不影响启动
        db_session.init_engine(settings)
        await init_db(settings)

        logger.info("%s v%s 启动完成", settings.app_name, settings.app_version)
        yield
        await db_session.dispose_engine()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="智能笔记 —— FastAPI + LangChain + Chroma 全栈笔记 + 知识库问答项目",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # 后 add 的最外层：request_id 覆盖所有请求（含 CORS 之前进入的）
    app.add_middleware(RequestContextMiddleware)

    # RAG 错误统一转成可读的 HTTP 响应（config -> 400，unavailable -> 503，限流 -> 429）
    app.add_exception_handler(RAGConfigurationError, rag_config_error_handler)
    app.add_exception_handler(RAGUnavailableError, rag_unavailable_error_handler)
    app.add_exception_handler(RateLimitExceeded, rate_limit_error_handler)

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
