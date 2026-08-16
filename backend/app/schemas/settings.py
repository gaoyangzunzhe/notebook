"""用户级设置 请求/响应模型。

响应绝不回传明文 API Key，只给 api_key_set 布尔标记。
各字段 None = 未设置（继承全局 .env）。
"""
from pydantic import BaseModel, Field, model_validator


class LlmSettings(BaseModel):
    provider: str | None = Field(default=None, max_length=32)  # null/"=继承 .env
    model: str | None = Field(default=None, max_length=64)
    base_url: str | None = Field(
        default=None,
        max_length=256,
        description="自定义接口地址（网关/代理），覆盖提供商注册表默认；空串/None=清除",
    )
    api_key: str | None = Field(default=None, description="明文密钥，仅写入用；空串=清除")
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)


class EmbedSettings(BaseModel):
    """嵌入模型配置（仅写入用）。provider null = 继承 .env。"""
    provider: str | None = Field(default=None, max_length=32)
    model: str | None = Field(default=None, max_length=64)
    base_url: str | None = Field(
        default=None,
        max_length=256,
        description="自定义接口地址（网关/代理），覆盖提供商注册表默认；空串/None=清除",
    )
    api_key: str | None = Field(default=None, description="明文密钥，仅写入用；空串=清除")


class KbSettings(BaseModel):
    top_k: int | None = Field(default=None, ge=1, le=20)
    chunk_size: int | None = Field(default=None, ge=200, le=8000)
    similarity_threshold: float | None = Field(default=None, ge=0.0, le=1.0)
    embed: EmbedSettings | None = None


class UiSettings(BaseModel):
    theme: str | None = Field(default=None, pattern="^(light|dark|system)$")
    sidebar_collapsed: bool | None = None


class SettingsUpdate(BaseModel):
    llm: LlmSettings | None = None
    kb: KbSettings | None = None
    ui: UiSettings | None = None

    @model_validator(mode="after")
    def _at_least_one_group(self) -> "SettingsUpdate":
        if self.llm is None and self.kb is None and self.ui is None:
            raise ValueError("至少提供一组设置（llm / kb / ui）")
        return self


class ProviderInfo(BaseModel):
    id: str
    name: str
    base_url: str
    models: list[str]


class LlmEffective(BaseModel):
    """当前真正生效的 LLM 配置（用户覆盖折叠后），用于前端回显实际使用值。"""
    provider: str | None = None  # 注册表 id；自定义 base_url 时为 None
    model: str | None = None
    base_url: str | None = None
    temperature: float | None = None
    api_key_set: bool = False
    warning: str | None = None  # 配置问题提示（如 key 与端点不匹配），None = 无


class LlmOut(BaseModel):
    # stored 覆盖值：None = 未覆盖（继承 .env），永不回传明文 Key
    provider: str | None = None
    model: str | None = None
    base_url: str | None = None
    api_key_set: bool = False
    temperature: float | None = None
    effective: LlmEffective | None = None


class EmbedEffective(BaseModel):
    """当前真正生效的嵌入配置（用户覆盖折叠后），用于前端回显实际使用值。"""
    provider: str | None = None
    model: str | None = None
    base_url: str | None = None
    api_key_set: bool = False
    warning: str | None = None  # 配置问题提示（如 key 与端点不匹配），None = 无


class EmbedOut(BaseModel):
    provider: str | None = None  # stored 覆盖值；None = 继承 .env
    model: str | None = None
    base_url: str | None = None
    api_key_set: bool = False
    effective: EmbedEffective | None = None


class ProviderModelsOut(BaseModel):
    """某提供商的模型列表（在线拉取或回退建议列表）。"""
    models: list[str]
    source: str = "fallback"  # live=GET /models 实时；fallback=注册表建议列表
    note: str | None = None  # 拉取失败/未配置 key 时的说明


class KbEffective(BaseModel):
    """当前真正生效的 RAG 标量参数。"""
    top_k: int
    chunk_size: int
    similarity_threshold: float | None = None


class KbOut(BaseModel):
    top_k: int | None = None
    chunk_size: int | None = None
    similarity_threshold: float | None = None
    embed: EmbedOut | None = None
    effective: KbEffective | None = None


class UiOut(BaseModel):
    theme: str | None = None
    sidebar_collapsed: bool | None = None


class SettingsOut(BaseModel):
    llm: LlmOut
    kb: KbOut
    ui: UiOut
    providers: list[ProviderInfo]
    embed_providers: list[ProviderInfo]
