"""Embedding 模型封装：OpenAI 兼容协议（DashScope / OpenAI / Ollama）。"""
from typing import Any

from langchain_openai import OpenAIEmbeddings

from app.core.config import Settings
from app.core.errors import RAGConfigurationError
from app.services.settings_service import _normalize_url


def get_embeddings(
    settings: Settings, *, overrides: dict[str, Any] | None = None
) -> OpenAIEmbeddings:
    """构建 OpenAIEmbeddings。

    overrides（来自用户级嵌入配置）优先级最高：提供 provider/model/api_key/base_url
    四键，其中 provider 只作日志/标记用，实际生效的是 model/api_key/base_url。
    Ollama 本地模型 api_key 为占位串 "ollama"，OpenAI SDK 只要求非空。

    check_embedding_ctx_length=False 是必须的：否则 OpenAIEmbeddings 会
    用 tiktoken 对输入做长度校验，该 tokenizer 对非 OpenAI 模型是错的。
    """
    model = (
        overrides.get("model") if overrides and overrides.get("model") else settings.embed_model
    )
    api_key = (
        overrides.get("api_key")
        if overrides and overrides.get("api_key")
        else settings.embed_api_key
    )
    base_url = (
        overrides.get("base_url")
        if overrides and overrides.get("base_url")
        else settings.embed_base_url
    )
    if not api_key:
        raise RAGConfigurationError(
            "嵌入模型 API Key 未配置（.env 的 EMBED_API_KEY 或用户设置），无法进行向量化"
        )
    if not base_url:
        # 有 key 但没地址：无法判断该 key 属于哪家端点，宁可报可读错误
        # 也不把 key 静默发往 OpenAI 官方地址（这是旧配置的隐蔽坑）。
        raise RAGConfigurationError(
            "嵌入模型接口地址（EMBED_BASE_URL）未配置，无法确定端点。"
            "请在 .env 设置 EMBED_BASE_URL，或在设置页选择嵌入提供商。"
        )
    # key 回退防护：选了非 .env 默认的嵌入端点，却复用了 .env 的默认密钥 -> 报可读错误。
    if (
        settings.embed_api_key
        and api_key == settings.embed_api_key
        and settings.embed_base_url
        and _normalize_url(base_url) != _normalize_url(settings.embed_base_url)
    ):
        raise RAGConfigurationError(
            "当前嵌入端点与 .env 默认提供商不同，但未填写该提供商的 API Key"
            "（正在复用 .env 的密钥，请求会失败）。请在设置页填写，"
            "或修改 .env 的 EMBED_API_KEY / EMBED_BASE_URL。"
        )
    return OpenAIEmbeddings(
        model=model,
        api_key=api_key,
        base_url=base_url,
        # 按提供商上限内部分批：DashScope 单次 ≤20，OpenAI 默认 1000 会直接超限
        chunk_size=settings.embed_batch_size,
        check_embedding_ctx_length=False,
    )
