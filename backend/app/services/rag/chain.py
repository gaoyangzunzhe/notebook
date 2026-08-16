"""LLM 与检索链构建：DeepSeek 对话模型 + RAG prompt。

注意：LangChain 1.x 中 create_retrieval_chain / create_stuff_documents_chain
迁移到了 langchain-classic 包（langchain_classic.chains.*）。
"""
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.core.config import Settings
from app.core.errors import RAGConfigurationError
from app.services.settings_service import _normalize_url

SYSTEM_PROMPT = """你是一个基于知识库回答问题的助手。请只根据提供的上下文内容回答问题，不要编造事实。
如果上下文中没有相关信息，请明确回答："我无法从知识库中找到相关信息"。
请使用与用户提问相同的语言回答。回答最后以"参考来源："开头，简要列出所引用的文档片段来源。"""

HUMAN_TEMPLATE = "问题：{input}\n\n上下文：\n{context}"


def get_llm(settings: Settings, *, overrides: dict | None = None) -> ChatOpenAI:
    """构建 OpenAI 兼容的 ChatOpenAI。

    overrides 是 {model, api_key, base_url, temperature} 四键字典，
    由 settings_service.resolve_llm 折叠用户级设置后传入；None 时用全局 .env。
    """
    cfg = overrides or {}
    api_key = cfg.get("api_key") or settings.llm_api_key
    base_url = cfg.get("base_url") or settings.llm_base_url
    if not api_key:
        raise RAGConfigurationError(
            "对话模型 API Key 未配置（.env 的 LLM_API_KEY 或用户设置）"
        )
    # key 回退防护：选了非 .env 默认的端点（其它提供商/自定义地址），
    # 却复用了 .env 的默认密钥 -> 直接报可读错误，而不是把 DeepSeek key 发到别处 401。
    if (
        settings.llm_api_key
        and api_key == settings.llm_api_key
        and settings.llm_base_url
        and _normalize_url(base_url) != _normalize_url(settings.llm_base_url)
    ):
        raise RAGConfigurationError(
            "当前模型端点与 .env 默认提供商不同，但未填写该提供商的 API Key"
            "（正在复用 .env 的密钥，请求会失败）。请在设置页填写该提供商的 Key，"
            "或修改 .env 的 LLM_API_KEY / LLM_BASE_URL。"
        )
    return ChatOpenAI(
        model=cfg.get("model") or settings.llm_model,
        api_key=api_key,
        base_url=base_url,
        temperature=cfg.get("temperature", settings.llm_temperature),
        # 请求超时 + 指数退避重试（OpenAI SDK 自带），防慢/挂起请求无限占用并发槽
        request_timeout=settings.llm_request_timeout,
        max_retries=settings.llm_max_retries,
    )


def build_retrieval_chain(
    settings: Settings, retriever, *, llm_overrides: dict | None = None
):
    """组装 RAG 检索链：retriever -> 上下文注入 -> LLM 生成。

    输入键为 input（新版本 langchain 的 create_retrieval_chain 约定），
    输出含 answer 与 context。llm_overrides 透传给 get_llm（用户级覆盖）。
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", HUMAN_TEMPLATE),
        ]
    )
    combine_docs_chain = create_stuff_documents_chain(
        get_llm(settings, overrides=llm_overrides), prompt
    )
    return create_retrieval_chain(retriever, combine_docs_chain)
