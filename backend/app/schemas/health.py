"""健康检查响应模型。"""
from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    components: dict[str, str]
    timestamp: datetime
