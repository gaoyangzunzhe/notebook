"""RAG 问答请求/响应模型。"""
from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4000, description="用户问题")
    session_id: str | None = Field(
        default=None, max_length=64, description="会话 ID，缺省时由后端生成"
    )
    # 缺省时后端按 user_settings.top_k -> 全局 retriever_k 解析
    k: int | None = Field(default=None, ge=1, le=20, description="召回文档块数量（可选）")
    category: str | None = Field(
        default=None, max_length=50, description="按知识库分类过滤，None=全部文档"
    )

    @field_validator("question")
    @classmethod
    def _strip_question(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("问题不能为空")
        return v


class SourceChunk(BaseModel):
    text: str
    source: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    session_id: str | None
    sources: list[SourceChunk]
