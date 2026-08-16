"""文档相关出入参模型：上传响应 + 管理（列表/详情）+ 分类。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    chunk_count: int
    db_persisted: bool


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    doc_id: str
    filename: str
    chunk_count: int
    category: str
    created_at: datetime


class DocumentListResponse(BaseModel):
    documents: list[DocumentOut]
    total: int
    db_available: bool = True


class DocumentCategoryUpdate(BaseModel):
    category: str = Field(..., min_length=1, max_length=50, description="新的文档分类")

    @field_validator("category")
    @classmethod
    def _strip(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("分类不能为空")
        return v


class CategoryCreate(BaseModel):
    category: str = Field(..., min_length=1, max_length=50, description="新建分类名")

    @field_validator("category")
    @classmethod
    def _strip(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("分类不能为空")
        return v


class CategoryListResponse(BaseModel):
    categories: list[str]
