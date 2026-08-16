"""RAG 相关异常与 FastAPI 异常处理器使用的错误类型。"""
from fastapi import Request
from fastapi.responses import JSONResponse


class RAGError(Exception):
    """RAG 错误基类。"""


class RAGConfigurationError(RAGError):
    """RAG 依赖未配置（例如缺少 API key）。"""


class RAGUnavailableError(RAGError):
    """RAG 提供方运行时失败（embedding/LLM/向量库不可用）。"""


def rag_config_error_handler(request: Request, exc: RAGConfigurationError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


def rag_unavailable_error_handler(request: Request, exc: RAGUnavailableError) -> JSONResponse:
    return JSONResponse(status_code=503, content={"detail": str(exc)})
