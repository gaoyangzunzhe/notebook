"""AI 写作辅助：续写 / 扩写 / 改写的提示词构造与流式生成。

设计要点：
- 人以笔记为主：prompt 明确要求模型延续用户语气，参考片段只是「可引用」的背景。
- 所有「可快速失败」的步骤（LLM 配置、向量检索、提示词构造）由路由在返回
  StreamingResponse 前完成；本模块只负责 token 流式产出。
- 事件协议：type=token 逐字增量 -> type=done 结束；中途异常 type=error 后结束。
"""
import asyncio
import json
import logging
from typing import AsyncIterator

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "你是一位协助用户撰写笔记的 AI 助手。用户是笔记的主要作者，"
    "请尊重并延续用户已有的语气与写作风格，用中文输出。"
)

# 截断后追加的省略标记
_OMIT_MARKER = "……（以下省略）"


def tail_truncate(text: str, limit: int) -> str:
    """保留末尾最多 limit 字符（续写时更贴近光标，相关性最高）。"""
    if len(text) <= limit:
        return text
    return "（前文省略）\n" + text[-limit:]


def _sentence_cut(text: str, limit: int) -> str:
    """按字符数截断，尽量在最近的行/句/词末截断。"""
    if len(text) <= limit:
        return text
    cut = text[:limit]
    for sep in ("\n", "。", "！", "？", " "):
        idx = cut.rfind(sep)
        if idx > limit * 3 // 4:
            cut = cut[: idx + 1]
            break
    return cut + _OMIT_MARKER


def format_context(chunks: list[tuple[object, float]], max_chars: int) -> str:
    """把检索到的 (Document, score) 格式化成语料片段，做总量预算。

    每块标注来源（文档名），总量不超过 max_chars；无片段返回空串
    （调用方据此决定是否注入"参考资料"段）。
    """
    if not chunks:
        return ""
    per_chunk = max_chars // len(chunks)
    parts: list[str] = []
    used = 0
    for i, (doc, _score) in enumerate(chunks, start=1):
        text = (doc.page_content or "").strip()  # type: ignore[attr-defined]
        if not text:
            continue
        source = doc.metadata.get("source") or doc.metadata.get("filename") or f"资料{i}"  # type: ignore[attr-defined]
        part = f"[{i}]（来源：{source}）{_sentence_cut(text, per_chunk)}"
        parts.append(part)
        used += len(part)
        if used >= max_chars:
            break
    return "\n\n".join(parts)


def build_messages(
    action: str,
    *,
    title: str,
    content_prefix: str = "",
    selected_text: str = "",
    instruction: str = "",
    context: str = "",
) -> list[dict]:
    """构造 chat messages。

    context 为已格式化的参考资料片段（可为空串）；非空时注入 system。
    action: continue（续写）/ expand（扩写）/ rewrite（改写）。
    """
    system = SYSTEM_PROMPT
    if context:
        system += (
            "\n\n可参考的文档资料片段（仅当与写作内容直接相关时可引用细节，"
            "不得虚构其中不存在的信息）：\n" + context
        )

    if action == "continue":
        user = (
            f"笔记标题：{title}\n\n以下是笔记当前内容（已截取到光标位置）：\n"
            f"{content_prefix}\n\n"
            "请从这段内容的结尾处自然地继续续写，延续主题与语气，不要重复或重述已有文字。"
        )
    elif action == "expand":
        user = (
            f"以下是从笔记《{title}》中选中的一段文字，请在不改变原意的前提下扩写："
            "补充细节、示例、论据或背景，使内容更充实。\n\n选中文字：\n" + selected_text
        )
    else:  # rewrite
        user = (
            f"以下是从笔记《{title}》中选中的一段文字，请改写："
            "保留原意，使表达更通顺、精炼。\n\n选中文字：\n" + selected_text
        )
    if instruction:
        user += f"\n\n用户额外要求：{instruction}"
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def _extract_text(chunk) -> str:
    """从 AIMessageChunk 抽取增量文本（兼容 str 与多模态 list 两种 content 形态）。"""
    content = chunk.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict) and item.get("type") == "text"
        )
    return str(content or "")


def _sse(data: dict) -> str:
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


async def stream_assist(
    llm,
    messages: list[dict],
    *,
    timeout_seconds: int = 120,
) -> AsyncIterator[str]:
    """流式生成 SSE 片段。调用方（路由）负责在进入本生成器前完成所有预检。

    - 正常结束：最后发一个 done 事件
    - 中途异常：发 error 事件后结束（不再发 done）
    - 客户端断开：asyncio.CancelledError 直接向上抛，由 Starlette 清理，不发 error
    """
    try:
        async with asyncio.timeout(timeout_seconds):
            async for chunk in llm.astream(messages):
                text = _extract_text(chunk)
                if text:
                    yield _sse({"type": "token", "content": text})
    except asyncio.CancelledError:
        logger.info("assist 流被客户端中断")
        raise
    except Exception as e:  # noqa: BLE001
        logger.warning("assist 生成中途失败: %s", e)
        try:
            yield _sse({"type": "error", "message": "生成中断，请重试"})
        except Exception:  # noqa: BLE001
            pass
        return
    yield _sse({"type": "done", "content": ""})
