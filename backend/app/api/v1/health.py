"""健康检查：进程活着就返回 200，组件状态仅供展示，不硬失败。"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.api.deps import db_status, get_settings, llm_status, vectorstore_status
from app.core.config import Settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        components={
            "db": await db_status(settings),
            "vectorstore": vectorstore_status(settings),
            "llm": llm_status(settings),
        },
        timestamp=datetime.now(timezone.utc),
    )
