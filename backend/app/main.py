"""FastAPI 应用工厂与入口。"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import Settings
from app.core.errors import (
    RAGConfigurationError,
    RAGUnavailableError,
    rag_config_error_handler,
    rag_unavailable_error_handler,
)
from app.core.logging import configure_logging
from app.db import session as db_session
from app.db.init_db import init_db

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        configure_logging(settings)
        settings.apply_runtime_env()
        app.state.settings = settings
        app.state.rag = None

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

    # RAG 错误统一转成可读的 HTTP 响应（config -> 400，unavailable -> 503）
    app.add_exception_handler(RAGConfigurationError, rag_config_error_handler)
    app.add_exception_handler(RAGUnavailableError, rag_unavailable_error_handler)

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
