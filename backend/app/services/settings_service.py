"""用户级设置解析：把 user_settings 行叠加到 .env 全局默认之上。

覆盖两套配置（语义一致）：
- 对话 LLM（PROVIDERS / resolve_llm / effective_llm）
- 嵌入模型（EMBED_PROVIDERS / resolve_embed / effective_embed）

语义约定：
- provider 为 NULL（未设置）时完全继承 .env（base_url/model/api_key/temperature）。
- provider 设了 -> 用对应注册表定 base_url（用户自定义 llm_base_url 优先）；model 缺省取该 provider 首个模型；
  API Key 解密失败或为空时回退 env key（Ollama 本地模型无 key，用占位串 "ollama"）；
  temperature 缺省回退 settings.llm_temperature。
- 所有解析都在端点层做，返回纯数据字典，绝不修改缓存的 RAGPipeline / Settings 对象。
"""
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.crypto import decrypt_secret
from app.models import UserSettings

# provider id -> {name, base_url, models}（models 列表顺序即前端下拉展示顺序）
# base_url / models 依据各官方 API 文档维护（2026-08 核实）：
#   DeepSeek  https://api-docs.deepseek.com        （chat/reasoner 别名 2026-07 弃用）
#   OpenAI    https://developers.openai.com/api/docs/models
#   Kimi      https://platform.kimi.com/docs/api/overview
#   智谱 GLM  https://docs.bigmodel.cn/cn/guide/models/text/glm-4
#   阿里百炼  https://www.alibabacloud.com/help/zh/model-studio/models
PROVIDERS: dict[str, dict[str, Any]] = {
    "deepseek": {
        "name": "DeepSeek",
        "base_url": "https://api.deepseek.com",
        "models": ["deepseek-v4-flash", "deepseek-v4-pro"],
    },
    "openai": {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "models": [
            "gpt-5.5",
            "gpt-5.4",
            "gpt-5.4-mini",
            "gpt-5.4-nano",
            "gpt-4.1",
            "gpt-4.1-mini",
        ],
    },
    "moonshot": {
        "name": "Kimi（月之暗面）",
        "base_url": "https://api.moonshot.cn/v1",
        "models": [
            "kimi-k2",
            "kimi-k2.5",
            "kimi-k2.6",
            "kimi-k2-thinking",
            "moonshot-v1-8k",
            "moonshot-v1-32k",
            "moonshot-v1-128k",
        ],
    },
    "zhipu": {
        "name": "智谱 GLM",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "models": ["glm-4-plus", "glm-4-air", "glm-4-flash", "glm-4-long", "glm-4-0520"],
    },
    "dashscope": {
        "name": "阿里云百炼（通义千问）",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "models": [
            "qwen-max-latest",
            "qwen-plus-latest",
            "qwen-turbo-latest",
            "qwen-flash-latest",
            "qwen-long-latest",
        ],
    },
    "ollama": {
        "name": "Ollama（本地）",
        "base_url": "http://localhost:11434/v1",
        # 本地模型列表因机器而异，这里只列常见建议；配合前端「自定义模型」输入任意本地模型 ID。
        "models": [
            "qwen2.5",
            "qwen2.5-coder",
            "qwen3",
            "llama3.1",
            "llama3.3",
            "gemma2",
            "mistral",
            "deepseek-r1",
        ],
    },
}

# 嵌入模型提供商注册表（embedding）。Ollama 本地模型无鉴权，API Key 自动用占位串。
EMBED_PROVIDERS: dict[str, dict[str, Any]] = {
    "dashscope": {
        "name": "阿里云百炼",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "models": ["text-embedding-v4", "text-embedding-v3", "text-embedding-v2"],
    },
    "openai": {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "models": [
            "text-embedding-3-large",
            "text-embedding-3-small",
            "text-embedding-ada-002",
        ],
    },
    "ollama": {
        "name": "Ollama（本地）",
        "base_url": "http://localhost:11434/v1",
        "models": ["nomic-embed-text", "bge-m3", "mxbai-embed-large"],
    },
}


async def get_user_settings(
    db_session: AsyncSession | None, user_id: int
) -> UserSettings | None:
    """按 user_id 取设置行；无库 / 无行返回 None（= 全继承 .env）。"""
    if db_session is None:
        return None
    result = await db_session.execute(
        select(UserSettings).where(UserSettings.user_id == user_id)
    )
    return result.scalar_one_or_none()


def resolve_top_k(
    request_k: int | None, us: UserSettings | None, settings: Settings
) -> int:
    """检索数优先级：请求显式 k -> 用户 top_k -> 全局 retriever_k。"""
    if request_k is not None:
        return request_k
    if us is not None and us.top_k is not None:
        return us.top_k
    return settings.retriever_k


def resolve_chunk_size(us: UserSettings | None, settings: Settings) -> int:
    """切分块大小：用户 chunk_size -> 全局 chunk_size。"""
    if us is not None and us.chunk_size is not None:
        return us.chunk_size
    return settings.chunk_size


def resolve_threshold(
    us: UserSettings | None, settings: Settings
) -> float | None:
    """相似度阈值：用户设置；None 表示不过滤（保持旧行为）。"""
    if us is not None and us.similarity_threshold is not None:
        return us.similarity_threshold
    return None


def resolve_llm(us: UserSettings | None, settings: Settings) -> dict[str, Any]:
    """把用户设置折叠成 get_llm 的 overrides 字典（四键全量给全）。"""
    if us is None or us.llm_provider is None:
        temperature = (
            us.temperature
            if us is not None and us.temperature is not None
            else settings.llm_temperature
        )
        return {
            "model": (
                us.llm_model if us is not None and us.llm_model else settings.llm_model
            ),
            "api_key": (
                decrypt_secret(settings, us.llm_api_key_encrypted)
                if us is not None and us.llm_api_key_encrypted
                else settings.llm_api_key
            ),
            "base_url": (
                us.llm_base_url if us is not None and us.llm_base_url else settings.llm_base_url
            ),
            "temperature": temperature,
        }
    provider = us.llm_provider
    info = PROVIDERS.get(provider)
    if info is None:
        # 理论上不会发生（PUT 已校验 provider ∈ PROVIDERS），防御性回退 .env
        return {
            "model": us.llm_model or settings.llm_model,
            "api_key": (
                decrypt_secret(settings, us.llm_api_key_encrypted)
                if us.llm_api_key_encrypted
                else settings.llm_api_key
            ),
            "base_url": us.llm_base_url or settings.llm_base_url,
            "temperature": (
                us.temperature if us.temperature is not None else settings.llm_temperature
            ),
        }
    api_key = settings.llm_api_key
    if us.llm_api_key_encrypted:
        decrypted = decrypt_secret(settings, us.llm_api_key_encrypted)
        if decrypted:
            api_key = decrypted
    if provider == "ollama":
        api_key = "ollama"  # 本地模型无需真实 key（OpenAI 客户端要求非空占位）
    return {
        "model": us.llm_model or info["models"][0],
        "api_key": api_key,
        "base_url": us.llm_base_url or info["base_url"],
        "temperature": (
            us.temperature if us.temperature is not None else settings.llm_temperature
        ),
    }


def _normalize_url(url: str) -> str:
    """归一化 base_url 用于比对：去尾部 / 与 /v1（如 api.deepseek.com/v1 == api.deepseek.com）。"""
    u = url.rstrip("/")
    if u.endswith("/v1"):
        u = u[:-3]
    return u


def match_env_provider(settings: Settings) -> str | None:
    """把 .env 的 base_url 匹配到注册表里的 provider id；匹配不上返回 None（自定义端点）。"""
    env_url = _normalize_url(settings.llm_base_url)
    for pid, info in PROVIDERS.items():
        if _normalize_url(info["base_url"]) == env_url:
            return pid
    return None


def llm_key_warning(us: UserSettings | None, settings: Settings) -> str | None:
    """检测 LLM 的 key 配置问题，返回可读提示（前端在设置页展示），None = 无问题。

    关键防护：用户选了非 .env 默认的端点（其它提供商/自定义地址）却没填它的 Key，
    解析会静默回退到 .env 的默认 key —— 这是「DeepSeek key 发到 OpenAI 端点 401」的根源。
    get_llm 会硬报错拦截，这里提前在回显里给出解释。
    """
    resolved = resolve_llm(us, settings)
    if not resolved["api_key"]:
        return "未配置对话模型 API Key：请在设置页填写，或配置 .env 的 LLM_API_KEY。"
    if (
        settings.llm_api_key
        and resolved["api_key"] == settings.llm_api_key
        and settings.llm_base_url
        and _normalize_url(resolved["base_url"]) != _normalize_url(settings.llm_base_url)
    ):
        env_provider = match_env_provider(settings)
        env_name = PROVIDERS[env_provider]["name"] if env_provider else "系统默认"
        return (
            f"当前 API Key 来自 .env 默认提供商（{env_name}），与所选端点"
            f"（{resolved['base_url']}）不匹配，调用会失败。请为该提供商填写自己的 API Key。"
        )
    return None


def effective_llm(us: UserSettings | None, settings: Settings) -> dict[str, Any]:
    """当前「真正生效」的 LLM 配置（用户覆盖折叠后），供 GET /settings 回显。

    与 llm 各字段（stored 覆盖值）区别：stored 的 None 表示「未覆盖」，
    effective 永远给出实际在用的 provider id / model / base_url / temperature / key 是否配置。
    """
    resolved = resolve_llm(us, settings)
    if us is not None and us.llm_provider:
        provider = us.llm_provider
    else:
        provider = match_env_provider(settings)
    return {
        "provider": provider,
        "model": resolved["model"],
        "base_url": resolved["base_url"],
        "temperature": resolved["temperature"],
        "api_key_set": bool(resolved["api_key"]) and resolved["api_key"] != "ollama",
        "warning": llm_key_warning(us, settings),
    }


# ---- 嵌入模型（embedding）：语义与 LLM 覆盖一致，provider 为 NULL 完全继承 .env ----

def match_env_embed_provider(settings: Settings) -> str | None:
    """把 .env 的 EMBED_BASE_URL 匹配到嵌入注册表 provider id；匹配不上返回 None。"""
    env_url = _normalize_url(settings.embed_base_url)
    for pid, info in EMBED_PROVIDERS.items():
        if _normalize_url(info["base_url"]) == env_url:
            return pid
    return None


def resolve_embed(us: UserSettings | None, settings: Settings) -> dict[str, Any]:
    """把用户嵌入设置折叠成 get_embeddings 的 overrides 字典（四键全给全）。"""
    if us is None or us.embed_provider is None:
        return {
            "provider": match_env_embed_provider(settings),
            "model": (
                us.embed_model if us is not None and us.embed_model else settings.embed_model
            ),
            "api_key": (
                decrypt_secret(settings, us.embed_api_key_encrypted)
                if us is not None and us.embed_api_key_encrypted
                else settings.embed_api_key
            ),
            "base_url": (
                us.embed_base_url if us is not None and us.embed_base_url else settings.embed_base_url
            ),
        }
    provider = us.embed_provider
    info = EMBED_PROVIDERS.get(provider)
    if info is None:
        # 理论上不会发生（PUT 已校验 provider ∈ EMBED_PROVIDERS），防御性回退 .env
        return {
            "provider": provider,
            "model": us.embed_model or settings.embed_model,
            "api_key": (
                decrypt_secret(settings, us.embed_api_key_encrypted)
                if us.embed_api_key_encrypted
                else settings.embed_api_key
            ),
            "base_url": us.embed_base_url or settings.embed_base_url,
        }
    api_key = settings.embed_api_key
    if us.embed_api_key_encrypted:
        decrypted = decrypt_secret(settings, us.embed_api_key_encrypted)
        if decrypted:
            api_key = decrypted
    if provider == "ollama":
        api_key = "ollama"  # 本地模型无需真实 key（OpenAI 客户端要求非空占位）
    return {
        "provider": provider,
        "model": us.embed_model or info["models"][0],
        "api_key": api_key,
        "base_url": us.embed_base_url or info["base_url"],
    }


def embed_key_warning(us: UserSettings | None, settings: Settings) -> str | None:
    """检测嵌入 key 的配置问题（语义同 llm_key_warning）。"""
    resolved = resolve_embed(us, settings)
    if not resolved["api_key"]:
        return "未配置嵌入模型 API Key：请在设置页填写，或配置 .env 的 EMBED_API_KEY。"
    if (
        settings.embed_api_key
        and resolved["api_key"] == settings.embed_api_key
        and settings.embed_base_url
        and _normalize_url(resolved["base_url"]) != _normalize_url(settings.embed_base_url)
    ):
        env_provider = match_env_embed_provider(settings)
        env_name = EMBED_PROVIDERS[env_provider]["name"] if env_provider else "系统默认"
        return (
            f"当前嵌入 API Key 来自 .env 默认提供商（{env_name}），与所选端点"
            f"（{resolved['base_url']}）不匹配，调用会失败。请为该提供商填写自己的 API Key。"
        )
    return None


def effective_embed(us: UserSettings | None, settings: Settings) -> dict[str, Any]:
    """当前真正生效的嵌入配置（含 provider 匹配），供 GET /settings 回显。"""
    resolved = resolve_embed(us, settings)
    return {
        "provider": resolved["provider"],
        "model": resolved["model"],
        "base_url": resolved["base_url"],
        "api_key_set": bool(resolved["api_key"]) and resolved["api_key"] != "ollama",
        "warning": embed_key_warning(us, settings),
    }


def effective_kb(us: UserSettings | None, settings: Settings) -> dict[str, Any]:
    """当前真正生效的 RAG 标量参数（top_k / chunk_size / similarity_threshold）。"""
    return {
        "top_k": resolve_top_k(None, us, settings),
        "chunk_size": resolve_chunk_size(us, settings),
        "similarity_threshold": resolve_threshold(us, settings),
    }
