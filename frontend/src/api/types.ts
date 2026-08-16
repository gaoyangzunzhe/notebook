// 后端 schema 的 TS 镜像（frontend 只读所需字段，字段名严格对齐 backend/app/schemas）

export interface User {
  id: number
  username: string
  email: string
  avatar: string | null
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

/* ---------------- 用户级设置（user_settings） ---------------- */

export interface ProviderInfo {
  id: string
  name: string
  base_url: string
  models: string[]
}

/** 当前真正生效的 LLM 配置（用户覆盖折叠后），用于回显实际使用值 */
export interface LlmEffective {
  provider: string | null
  model: string | null
  base_url: string | null
  temperature: number | null
  api_key_set: boolean
  /** 配置问题提示（如 key 与端点不匹配），null = 无 */
  warning: string | null
}

export interface LlmOut {
  /** stored 覆盖值：null = 未覆盖（继承 .env） */
  provider: string | null
  model: string | null
  /** stored 自定义接口地址：null = 未覆盖（用提供商/系统默认地址） */
  base_url: string | null
  api_key_set: boolean
  temperature: number | null
  effective: LlmEffective
}

/** 当前真正生效的嵌入配置（用户覆盖折叠后），用于回显实际使用值 */
export interface EmbedEffective {
  provider: string | null
  model: string | null
  base_url: string | null
  api_key_set: boolean
  /** 配置问题提示（如 key 与端点不匹配），null = 无 */
  warning: string | null
}

/** 嵌入模型覆盖：provider 为 null = 继承 .env */
export interface EmbedOut {
  provider: string | null
  model: string | null
  /** stored 自定义接口地址：null = 未覆盖 */
  base_url: string | null
  api_key_set: boolean
  effective: EmbedEffective
}

/** 某提供商的模型列表（在线拉取 live / 注册表建议 fallback） */
export interface ProviderModelsOut {
  models: string[]
  source: 'live' | 'fallback'
  note: string | null
}

/** 当前真正生效的 RAG 标量参数 */
export interface KbEffective {
  top_k: number
  chunk_size: number
  similarity_threshold: number | null
}

export interface KbOut {
  top_k: number | null
  chunk_size: number | null
  similarity_threshold: number | null
  embed: EmbedOut
  effective: KbEffective
}

export interface UiOut {
  theme: string | null
  sidebar_collapsed: boolean | null
}

export interface SettingsOut {
  llm: LlmOut
  kb: KbOut
  ui: UiOut
  providers: ProviderInfo[]
  embed_providers: ProviderInfo[]
}

export interface SettingsUpdatePayload {
  llm?: {
    provider?: string | null
    model?: string | null
    base_url?: string | null
    api_key?: string
    temperature?: number | null
  }
  kb?: {
    /** null = 清除覆盖回退系统默认 */
    top_k?: number | null
    chunk_size?: number | null
    similarity_threshold?: number | null
    embed?: {
      provider?: string | null
      model?: string | null
      base_url?: string | null
      api_key?: string
    }
  }
  ui?: {
    theme?: string
    sidebar_collapsed?: boolean
  }
}

export interface DocumentRecord {
  doc_id: string
  filename: string
  chunk_count: number
  category: string
  created_at: string
}

export interface DocumentCategoryUpdate {
  category: string
}

export interface CategoryListResponse {
  categories: string[]
}

export interface DocumentListResponse {
  documents: DocumentRecord[]
  total: number
  db_available: boolean
}

export interface UploadResponse {
  doc_id: string
  filename: string
  chunk_count: number
  db_persisted: boolean
}

export interface SourceChunk {
  text: string
  source: string
  score: number
}

export interface QueryResponse {
  answer: string
  session_id: string | null
  sources: SourceChunk[]
}

export interface MessageRecord {
  id: number
  role: 'user' | 'assistant' | string
  content: string
  created_at: string
}

/** 前端气泡消息：在 MessageRecord 基础上附加渲染用字段 */
export interface ChatMessage extends MessageRecord {
  sources?: SourceChunk[]
  pending?: boolean
}

export interface ChatHistoryResponse {
  session_id: string
  db_available: boolean
  messages: MessageRecord[]
}

export interface SessionSummary {
  session_id: string
  title: string
  last_message: string
  message_count: number
  updated_at: string
}

export interface ChatSessionsResponse {
  sessions: SessionSummary[]
  total: number
  db_available: boolean
}

export interface HealthResponse {
  status: string
  service: string
  version: string
  components: Record<string, string>
  timestamp: string
}

/* ---------------- 笔记 / 相关文档 / 分类 / assist ---------------- */

export const NOTE_TAGS = ['工作', '学习', '生活', '技术', '其他'] as const
export type NoteTag = (typeof NOTE_TAGS)[number]

export interface NoteOut {
  id: number
  title: string
  content: string
  tag: string | null
  created_at: string
  updated_at: string
}

export interface NoteListResponse {
  notes: NoteOut[]
  total: number
}

export interface NoteCreate {
  title: string
  content?: string
}

export interface NoteUpdate {
  title?: string
  content?: string
  tag?: string
}

/** 「相关文档」推荐项：用笔记正文临时检索知识库，不持久化、无硬关联 */
export interface RelatedDocumentOut {
  doc_id: string
  filename: string
  score: number
  chunk_count: number
}

export interface RelatedDocumentListResponse {
  related: RelatedDocumentOut[]
}

export interface TagResponse {
  tag: string
}

export type AssistAction = 'continue' | 'expand' | 'rewrite'

export interface AssistRequest {
  action: AssistAction
  /** 扩写/改写必填（非空） */
  selected_text?: string
  /** 仅 continue 使用，>=0，后端会 clamp 到笔记长度 */
  cursor_position?: number
  /** 可选，<=500 */
  instruction?: string
}

export type AssistEvent =
  | { type: 'token'; content: string }
  | { type: 'done'; content: string }
  | { type: 'error'; message: string }
