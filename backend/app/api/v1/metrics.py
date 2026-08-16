"""基础指标快照（公开端点，仅聚合数据，不含任何用户信息）。"""
from fastapi import APIRouter

from app.core import metrics

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
async def get_metrics() -> dict:
    return metrics.snapshot()
