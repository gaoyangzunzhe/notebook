"""笔记标签分类：LLM 归入固定五类，非法输出回退「其他」。

系统提示词由 NOTE_TAGS 拼接生成（单一来源，避免集合漂移）。
"""
import asyncio
import logging

from app.core.config import Settings
from app.core.errors import RAGUnavailableError
from app.models import NOTE_TAGS
from app.services.rag.chain import get_llm

logger = logging.getLogger(__name__)

# 输出清洗时剥掉的外围标点 / 引号（不要求全量）
_STRIP_CHARS = '“”"\'。．,，;；:：【】 \t\r\n'


def _system_prompt() -> str:
    return (
        "你是一个笔记标签分类器。请把用户笔记归入且仅归入以下五个标签之一："
        + "、".join(NOTE_TAGS)
        + "。只输出标签名本身，不要包含任何解释、标点或多余文字。"
    )


def _normalize(raw: str) -> str:
    """清洗模型输出，返回合法标签；无法精确匹配则回退「其他」。"""
    cleaned = (raw or "").strip().strip(_STRIP_CHARS)
    return cleaned if cleaned in NOTE_TAGS else "其他"


async def classify_tag(
    settings: Settings, title: str, content: str, *, llm=None
) -> str:
    """用 LLM 把笔记归入固定五类并返回标签名。

    调用方可用用户级 overrides 构建好的 llm 传入；缺省时按全局 .env 构建。
    api_key 缺失 -> RAGConfigurationError（路由转 400）；调用失败/超时
    -> RAGUnavailableError（路由转 503）。输出经 _normalize 保证合法。
    """
    llm = llm or get_llm(settings)
    messages = [
        {"role": "system", "content": _system_prompt()},
        {"role": "user", "content": f"笔记标题：{title}\n\n笔记内容：\n{content}"},
    ]
    try:
        async with asyncio.timeout(30):
            resp = await llm.ainvoke(messages)
    except Exception as e:  # noqa: BLE001
        logger.warning("标签分类调用失败: %s", e)
        raise RAGUnavailableError(f"标签分类调用失败: {e}") from e
    raw = resp.content if isinstance(resp.content, str) else str(resp.content or "")
    return _normalize(raw)
