"""全局配置：所有配置从 backend/.env 读取（pydantic-settings）。"""
import os
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/ 目录的绝对路径（与 cwd 无关，保证任意目录启动都能读到 .env）
BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """应用配置。

    字段与 backend/.env 的键一一对应（pydantic-settings 大小写不敏感，
    因此 LLM_API_KEY -> llm_api_key，EMBED_MODEL -> embed_model）。
    统一前缀：LLM_* 对话模型，EMBED_* 嵌入模型。
    所有字段都有安全默认值：缺 key 不崩溃，RAG 相关能力在使用时校验。
    """

    model_config = SettingsConfigDict(
        env_file=BACKEND_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ---- 对话模型（默认 DeepSeek，OpenAI 兼容协议）----
    # 统一前缀：LLM_* 描述对话模型，EMBED_* 描述嵌入模型，杜绝歧义。
    # 这些是全局默认值（.env）；用户可在设置页配置自己的 provider/model/base_url/Key，
    # 覆盖后存 user_settings 表（Key 用 SECRET_KEY 派生密钥加密存储）。
    llm_api_key: str = ""
    llm_base_url: str = "https://api.deepseek.com"
    llm_model: str = "deepseek-v4-flash"
    llm_temperature: float = 0.2  # 全局默认生成温度（用户级 user_settings.temperature 可覆盖）

    # ---- 嵌入模型（默认 DashScope / 阿里云百炼，OpenAI 兼容协议）----
    embed_model: str = "text-embedding-v4"
    embed_api_key: str = ""
    embed_base_url: str = ""  # 为空且 key 已配置时在 embeddings.py 显式报错，避免静默发往 OpenAI 官方端点
    # 单次嵌入请求的批量上限：DashScope 限制 ≤20，OpenAI 更高（2048）。
    # langchain OpenAIEmbeddings 用它做内部分批，超限的文档会被拆成多次请求。
    embed_batch_size: int = 20

    # ---- LangSmith 链路追踪（LangChain 只读 os.environ，见 apply_runtime_env）----
    langchain_tracing_v2: bool = False
    langchain_project: str = "notebook_rag"
    langchain_api_key: str = ""

    # ---- 关系数据库（懒连接：启动时不强连）----
    database_url: str = ""

    # ---- Redis（可选）：配置后启用缓存（提供商模型列表等）；为空 = 缓存禁用，功能不受影响 ----
    redis_url: str = ""

    # ---- 认证（JWT）----
    # SECRET_KEY 生产环境必须用强随机密钥；dev 默认值仅保证 .env 缺失时也能启动
    secret_key: str = "dev-insecure-secret-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24h

    # ---- CORS（Vite dev server 端口；多个来源用英文逗号分隔）----
    cors_origins: list[str] = ["http://localhost:5173"]

    # ---- 切分与检索默认值（后续可拓展到配置项）----
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retriever_k: int = 4

    # ---- AI 写作辅助预算 ----
    assist_max_note_chars: int = 8000  # 续写时传给模型的笔记正文截断上限
    assist_max_context_chars: int = 3200  # 参考资料片段总量预算
    assist_timeout_seconds: int = 120  # 单次 assist 流式生成总预算

    # ---- AI 调用护栏（LLM/嵌入是成本与并发大头，按用户限流 + 全局并发上限）----
    ai_quota_limit: int = 30  # 每用户每小时 AI 调用上限（RAG 提问/辅助写作/自动分类/上传），0 = 关闭
    ai_quota_window_seconds: int = 3600
    ai_max_concurrent_llm: int = 4  # 全局并发 LLM/嵌入调用上限（防重试风暴打爆成本/厂商 429）
    llm_request_timeout: int = 120  # 单次 LLM 请求超时（秒）
    llm_max_retries: int = 2  # OpenAI SDK 指数退避重试次数
    embed_request_timeout: int = 120  # 单次嵌入请求超时（秒）
    embed_max_retries: int = 2

    # ---- 模型列表缓存（Redis，可选；未配置 REDIS_URL 时缓存自动失效，功能不受影响）----
    model_cache_ttl_seconds: int = 300  # 提供商模型列表在线拉取缓存时长

    # ---- 应用元信息 ----
    app_name: str = "notebook-api"
    app_version: str = "0.1.0"

    @field_validator("database_url", mode="after")
    @classmethod
    def _fix_asyncpg_driver_typo(cls, v: str) -> str:
        """修复 .env 中 asycopg2 -> asyncpg 的驱动名笔误。"""
        if v and v.startswith("postgresql+asycopg2://"):
            v = v.replace("postgresql+asycopg2://", "postgresql+asyncpg://", 1)
        return v

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, v: object) -> object:
        """把逗号分隔的字符串解析成列表，兼容 JSON 数组形式。"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @property
    def sync_database_url(self) -> str:
        """同步驱动 URL（仅在后续引入 psycopg2 时使用）。"""
        return self.database_url.replace("+asyncpg://", "+psycopg2://", 1)

    # ---- 路径助手（一律绝对路径，Chroma 在 Windows 上对相对路径不可靠）----
    @property
    def data_dir(self) -> Path:
        return BACKEND_ROOT / "data"

    @property
    def chroma_dir(self) -> Path:
        return self.data_dir / "chroma"

    @property
    def upload_dir(self) -> Path:
        return self.data_dir / "uploads"

    def apply_runtime_env(self) -> None:
        """把 LangSmith 配置写进 os.environ。

        LangChain 只在 os.environ 里读取 LANGCHAIN_* 变量，不会去读 .env，
        因此必须在启动时显式注入，否则 tracing 会静默失效。
        """
        os.environ.setdefault(
            "LANGCHAIN_TRACING_V2", "true" if self.langchain_tracing_v2 else "false"
        )
        os.environ.setdefault("LANGCHAIN_PROJECT", self.langchain_project)
        if self.langchain_api_key:
            os.environ.setdefault("LANGCHAIN_API_KEY", self.langchain_api_key)
