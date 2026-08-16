"""用户级设置：GET 回读 / PUT 部分更新（upsert）。

GET 回 stored 值（None = 继承全局）、api_key_set 标记与 effective（当前实际生效配置），
永不回传明文 Key。PUT 按组（llm / kb / ui）部分更新，至少一组；
provider 校验 ∈ PROVIDERS（模型不设白名单），字段按「显式出现」更新，null=清除覆盖。
"""
import hashlib
import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

# get_settings 别名 get_app_settings：本模块的 GET 端点也叫 get_settings，
# 若不改名，PUT 端点的 Depends(get_settings) 会解析到端点函数本身。
from app.api.deps import get_current_user, get_settings as get_app_settings
from app.core.cache import cache_get, cache_set
from app.core.config import Settings
from app.core.crypto import decrypt_secret, encrypt_secret
from app.db.session import get_db
from app.models import User, UserSettings
from app.schemas.settings import (
    EmbedEffective,
    EmbedOut,
    KbEffective,
    KbOut,
    LlmEffective,
    LlmOut,
    LlmSettings,
    ProviderInfo,
    ProviderModelsOut,
    SettingsOut,
    SettingsUpdate,
    UiOut,
)
from app.services.settings_service import (
    EMBED_PROVIDERS,
    PROVIDERS,
    _normalize_url,
    effective_embed,
    effective_kb,
    effective_llm,
    match_env_embed_provider,
    match_env_provider,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/settings", tags=["settings"])


async def _require_db(db_session: AsyncSession | None) -> AsyncSession:
    if db_session is None:
        raise HTTPException(status_code=503, detail="设置服务不可用：数据库未配置")
    return db_session


async def _get_row(session: AsyncSession, user_id: int) -> UserSettings | None:
    result = await session.execute(
        select(UserSettings).where(UserSettings.user_id == user_id)
    )
    return result.scalar_one_or_none()


def _providers_out() -> list[ProviderInfo]:
    return [
        ProviderInfo(
            id=pid,
            name=info["name"],
            base_url=info["base_url"],
            models=list(info["models"]),
        )
        for pid, info in PROVIDERS.items()
    ]


def _embed_providers_out() -> list[ProviderInfo]:
    return [
        ProviderInfo(
            id=pid,
            name=info["name"],
            base_url=info["base_url"],
            models=list(info["models"]),
        )
        for pid, info in EMBED_PROVIDERS.items()
    ]


def _llm_out(row: UserSettings | None, settings: Settings) -> LlmOut:
    if row is None:
        return LlmOut(
            provider=None,
            model=None,
            base_url=None,
            api_key_set=False,
            temperature=None,
            effective=LlmEffective(**effective_llm(None, settings)),
        )
    return LlmOut(
        provider=row.llm_provider,
        model=row.llm_model,
        base_url=row.llm_base_url,
        api_key_set=bool(row.llm_api_key_encrypted),
        temperature=row.temperature,
        effective=LlmEffective(**effective_llm(row, settings)),
    )


def _embed_out(row: UserSettings | None, settings: Settings) -> EmbedOut:
    if row is None:
        return EmbedOut(
            provider=None,
            model=None,
            base_url=None,
            api_key_set=False,
            effective=EmbedEffective(**effective_embed(None, settings)),
        )
    return EmbedOut(
        provider=row.embed_provider,
        model=row.embed_model,
        base_url=row.embed_base_url,
        api_key_set=bool(row.embed_api_key_encrypted),
        effective=EmbedEffective(**effective_embed(row, settings)),
    )


def _kb_out(row: UserSettings | None, settings: Settings) -> KbOut:
    return KbOut(
        top_k=row.top_k if row is not None else None,
        chunk_size=row.chunk_size if row is not None else None,
        similarity_threshold=row.similarity_threshold if row is not None else None,
        embed=_embed_out(row, settings),
        effective=KbEffective(**effective_kb(row, settings)),
    )


def _to_out(row: UserSettings | None, settings: Settings) -> SettingsOut:
    return SettingsOut(
        llm=_llm_out(row, settings),
        kb=_kb_out(row, settings),
        ui=(
            UiOut(theme=row.theme, sidebar_collapsed=row.sidebar_collapsed)
            if row is not None
            else UiOut(theme=None, sidebar_collapsed=None)
        ),
        providers=_providers_out(),
        embed_providers=_embed_providers_out(),
    )


def _validate_llm(v: LlmSettings) -> None:
    """provider 必须先于任何 DB 写入校验。模型只做非空校验，不设白名单——
    注册表 models 是「建议列表」，各厂商会随时上新模型，用户可能存注册表之外的模型 ID。"""
    if v.provider and v.provider not in PROVIDERS:
        raise HTTPException(status_code=422, detail="不支持的 AI 提供商")


def _apply_llm(row: UserSettings, v: LlmSettings, settings: Settings) -> None:
    """按「显式出现的字段」部分更新；None = 清除覆盖回退 .env。"""
    if "provider" in v.model_fields_set:
        if not v.provider:
            # 清空 provider -> 连带清 model/base_url 与 key，完全继承 .env
            row.llm_provider = None
            row.llm_model = None
            row.llm_base_url = None
            row.llm_api_key_encrypted = None
        else:
            row.llm_provider = v.provider
    if "base_url" in v.model_fields_set:
        row.llm_base_url = (v.base_url or "").strip() or None
    if "model" in v.model_fields_set and v.model:
        row.llm_model = v.model
    if "api_key" in v.model_fields_set and v.api_key is not None:
        if v.api_key == "":
            row.llm_api_key_encrypted = None
        else:
            row.llm_api_key_encrypted = encrypt_secret(settings, v.api_key)
    if "temperature" in v.model_fields_set:
        row.temperature = v.temperature


def _validate_embed(v) -> None:
    if v.provider and v.provider not in EMBED_PROVIDERS:
        raise HTTPException(status_code=422, detail="不支持的嵌入提供商")


def _apply_kb(row: UserSettings, v, settings: Settings) -> None:
    # 与 _apply_llm 一致：按「显式出现的字段」更新，null = 清除覆盖回退全局
    if "top_k" in v.model_fields_set:
        row.top_k = v.top_k
    if "chunk_size" in v.model_fields_set:
        row.chunk_size = v.chunk_size
    if "similarity_threshold" in v.model_fields_set:
        row.similarity_threshold = v.similarity_threshold
    if v.embed is not None:
        emb = v.embed
        if "provider" in emb.model_fields_set:
            if not emb.provider:
                # 清空嵌入覆盖 -> 完全继承 .env
                row.embed_provider = None
                row.embed_model = None
                row.embed_base_url = None
                row.embed_api_key_encrypted = None
            else:
                row.embed_provider = emb.provider
        if "base_url" in emb.model_fields_set:
            row.embed_base_url = (emb.base_url or "").strip() or None
        if "model" in emb.model_fields_set and emb.model:
            row.embed_model = emb.model
        if "api_key" in emb.model_fields_set and emb.api_key is not None:
            if emb.api_key == "":
                row.embed_api_key_encrypted = None
            else:
                row.embed_api_key_encrypted = encrypt_secret(settings, emb.api_key)


def _apply_ui(row: UserSettings, v) -> None:
    if v.theme is not None:
        row.theme = v.theme
    if v.sidebar_collapsed is not None:
        row.sidebar_collapsed = v.sidebar_collapsed


@router.get("", response_model=SettingsOut)
async def get_settings(
    current_user: User = Depends(get_current_user),
    settings: Settings = Depends(get_app_settings),
    db_session: AsyncSession | None = Depends(get_db),
) -> SettingsOut:
    """回读当前用户设置（stored 字段 None = 继承 .env；key 只给 api_key_set；附带 effective）。"""
    session = await _require_db(db_session)
    try:
        row = await _get_row(session, current_user.id)
    except SQLAlchemyError as e:
        logger.warning("查询用户设置失败: %s", e)
        raise HTTPException(status_code=503, detail="设置服务不可用：数据库连接失败")
    return _to_out(row, settings)


@router.put("", response_model=SettingsOut)
async def update_settings(
    body: SettingsUpdate,
    current_user: User = Depends(get_current_user),
    settings: Settings = Depends(get_app_settings),
    db_session: AsyncSession | None = Depends(get_db),
) -> SettingsOut:
    """按组部分更新设置；无行则 upsert 新建（一行/用户）。"""
    session = await _require_db(db_session)
    if body.llm is not None:
        _validate_llm(body.llm)
    if body.kb is not None and body.kb.embed is not None:
        _validate_embed(body.kb.embed)
    try:
        row = await _get_row(session, current_user.id)
        if row is None:
            row = UserSettings(user_id=current_user.id)
            session.add(row)
        if body.llm is not None:
            _apply_llm(row, body.llm, settings)
        if body.kb is not None:
            _apply_kb(row, body.kb, settings)
        if body.ui is not None:
            _apply_ui(row, body.ui)
        await session.commit()
        await session.refresh(row)
        return _to_out(row, settings)
    except SQLAlchemyError as e:
        await session.rollback()
        logger.warning("写入用户设置失败: %s", e)
        raise HTTPException(status_code=503, detail="设置服务不可用：数据库连接失败")


@router.get("/providers/{kind}/{provider_id}/models", response_model=ProviderModelsOut)
async def provider_models(
    kind: str,
    provider_id: str,
    base_url: str | None = Query(default=None, max_length=256),
    current_user: User = Depends(get_current_user),
    settings: Settings = Depends(get_app_settings),
    db_session: AsyncSession | None = Depends(get_db),
) -> ProviderModelsOut:
    """在线拉取某提供商的模型列表（GET {base_url}/models，OpenAI 兼容协议）。

    解决「注册表硬编码模型列表过期」问题（参考 LibreChat 的 models.fetch 思路）：
    - 优先用已保存的配置（用户自定义 base_url / 用户 Key / env 默认）请求 /models；
    - 失败或未配置 key 时回退注册表建议列表，附原因；
    - base_url 查询参数 = 前端当前输入框的「预览地址」：与已保存端点不一致时不携带密钥，
      避免把密钥发到任意用户输入的地址（SSRF/泄密防护）。
    """
    kind = kind.lower()
    if kind == "llm":
        info = PROVIDERS.get(provider_id)
        env_key = settings.llm_api_key
        env_provider = match_env_provider(settings)
        us: UserSettings | None = None
        if db_session is not None:
            try:
                us = await _get_row(db_session, current_user.id)
            except SQLAlchemyError as e:
                logger.debug("读取用户设置失败（回退 env 配置）: %s", e)
        user_key = decrypt_secret(settings, us.llm_api_key_encrypted) if us and us.llm_api_key_encrypted else None
        saved_custom = us.llm_base_url if us else None
    elif kind == "embed":
        info = EMBED_PROVIDERS.get(provider_id)
        env_key = settings.embed_api_key
        env_provider = match_env_embed_provider(settings)
        us = None
        if db_session is not None:
            try:
                us = await _get_row(db_session, current_user.id)
            except SQLAlchemyError as e:
                logger.debug("读取用户设置失败（回退 env 配置）: %s", e)
        user_key = decrypt_secret(settings, us.embed_api_key_encrypted) if us and us.embed_api_key_encrypted else None
        saved_custom = us.embed_base_url if us else None
    else:
        raise HTTPException(status_code=422, detail="kind 必须为 llm 或 embed")
    if info is None:
        raise HTTPException(status_code=404, detail="不支持的提供商")

    resolved_base = saved_custom or info["base_url"]
    target_base = (base_url or "").strip() or resolved_base

    # key：用户覆盖 key 优先；ollama 占位；否则仅当该提供商就是 env 默认时才复用 env key
    api_key = user_key or None
    if not api_key:
        if provider_id == "ollama":
            api_key = "ollama"
        elif env_provider == provider_id:
            api_key = env_key

    # 预览地址 != 已保存端点：不携带密钥（避免把密钥发往任意输入地址）
    if _normalize_url(target_base) != _normalize_url(resolved_base):
        api_key = None

    # 缓存（Redis，可选）：key 只含 base_url + 是否有 key + 注册表指纹，不含密钥明文；
    # 未配置 REDIS_URL 时 cache_get 恒返回 None，直接走在线拉取。
    cache_key = "models:{0}:{1}:{2}".format(
        target_base,
        "key" if api_key else "nokey",
        hashlib.md5("|".join(info["models"]).encode()).hexdigest()[:8],
    )
    cached = await cache_get(settings, cache_key)
    if cached is not None:
        try:
            return ProviderModelsOut.model_validate_json(cached)
        except Exception:  # noqa: BLE001
            logger.debug("模型列表缓存反序列化失败，忽略缓存")

    result = await _fetch_provider_models(target_base, api_key, list(info["models"]))
    await cache_set(
        settings, cache_key, result.model_dump_json(), settings.model_cache_ttl_seconds
    )
    return result


async def _fetch_provider_models(
    base_url: str, api_key: str | None, registry_models: list[str]
) -> ProviderModelsOut:
    """请求 GET {base_url}/models 拉模型列表；失败/无 key 回退注册表建议列表并附说明。"""
    if not api_key:
        return ProviderModelsOut(
            models=registry_models,
            source="fallback",
            note="未配置该提供商的 API Key，无法在线拉取，显示建议列表。",
        )
    url = base_url.rstrip("/") + "/models"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                url, headers={"Authorization": f"Bearer {api_key}"}
            )
            resp.raise_for_status()
            data = resp.json()
        ids = [m["id"] for m in data.get("data", []) if m.get("id")]
        if not ids:
            return ProviderModelsOut(
                models=registry_models,
                source="fallback",
                note="模型端点未返回可用模型，显示建议列表。",
            )
        return ProviderModelsOut(models=sorted(ids), source="live")
    except Exception as e:  # noqa: BLE001
        logger.debug("在线拉取模型列表失败（%s）: %s", base_url, e)
        return ProviderModelsOut(
            models=registry_models,
            source="fallback",
            note="在线拉取失败（{0}），显示建议列表。".format(type(e).__name__),
        )
