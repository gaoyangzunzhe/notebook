"""笔记、文档关联、AI 写作辅助与标签出入参模型。"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models import NOTE_TAGS


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(default="", max_length=100_000)

    @field_validator("title")
    @classmethod
    def _strip_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("笔记标题不能为空")
        return v


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = Field(default=None, max_length=100_000)
    tag: str | None = Field(default=None, max_length=16)

    @field_validator("title")
    @classmethod
    def _strip_title(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("笔记标题不能为空")
        return v

    @field_validator("tag")
    @classmethod
    def _check_tag(cls, v: str | None) -> str | None:
        if v is not None and v not in NOTE_TAGS:
            raise ValueError(f"分类必须是 {NOTE_TAGS} 之一")
        return v

    @model_validator(mode="after")
    def _at_least_one(self) -> "NoteUpdate":
        if self.title is None and self.content is None and self.tag is None:
            raise ValueError("至少提供一个待更新字段")
        return self


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    tag: str | None
    created_at: datetime
    updated_at: datetime


class NoteListResponse(BaseModel):
    notes: list[NoteOut]
    total: int


class RelatedDocumentOut(BaseModel):
    """「相关文档」推荐项：用笔记正文对知识库临时检索的结果，不持久化。"""

    doc_id: str
    filename: str
    score: float
    chunk_count: int


class RelatedDocumentListResponse(BaseModel):
    related: list[RelatedDocumentOut]


class AssistAction(str, Enum):
    continue_writing = "continue"  # 续写
    expand = "expand"  # 扩写
    rewrite = "rewrite"  # 改写 / 重写


class AssistRequest(BaseModel):
    action: AssistAction
    selected_text: str | None = Field(default=None, max_length=20_000)
    cursor_position: int | None = Field(default=None, ge=0)
    instruction: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def _check_action(self) -> "AssistRequest":
        if self.action in (AssistAction.expand, AssistAction.rewrite):
            if not self.selected_text or not self.selected_text.strip():
                raise ValueError("扩写/改写必须提供选中的文本 selected_text")
        return self


class TagResponse(BaseModel):
    tag: str
