"""v1 路由聚合：统一在 /api/v1 下挂载各业务模块。"""
from fastapi import APIRouter

from app.api.v1 import (
    auth,
    chat,
    documents,
    health,
    notes,
    rag,
    settings,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(documents.router)
api_router.include_router(rag.router)
api_router.include_router(settings.router)
api_router.include_router(chat.router)
api_router.include_router(notes.router)
