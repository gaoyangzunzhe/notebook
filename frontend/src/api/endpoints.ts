import { apiClient } from './client'
import type {
  CategoryListResponse,
  ChatHistoryResponse,
  ChatSessionsResponse,
  DocumentListResponse,
  DocumentRecord,
  HealthResponse,
  NoteCreate,
  NoteListResponse,
  NoteOut,
  NoteUpdate,
  ProviderModelsOut,
  QueryResponse,
  RelatedDocumentListResponse,
  SettingsOut,
  SettingsUpdatePayload,
  TagResponse,
  TokenResponse,
  UploadResponse,
  User,
} from './types'

export const authApi = {
  register: (
    username: string,
    email: string,
    password: string,
    confirmPassword: string,
  ) =>
    apiClient.post<User>('/auth/register', {
      username,
      email,
      password,
      confirm_password: confirmPassword,
    }),
  login: (account: string, password: string) =>
    apiClient.post<TokenResponse>('/auth/login', { account, password }),
  me: () => apiClient.get<User>('/auth/me'),
  updateUsername: (username: string) =>
    apiClient.patch<User>('/auth/me', { username }),
  changePassword: (
    oldPassword: string,
    newPassword: string,
    confirmPassword: string,
  ) =>
    apiClient.post<void>('/auth/password', {
      old_password: oldPassword,
      new_password: newPassword,
      confirm_password: confirmPassword,
    }),
  uploadAvatar: (file: File) => {
    const form = new FormData()
    form.append('file', file) // 字段名须匹配后端 UploadFile(...)
    return apiClient.post<User>('/auth/avatar', form)
  },
  deleteAvatar: () => apiClient.delete<void>('/auth/avatar'),
}

export const settingsApi = {
  get: () => apiClient.get<SettingsOut>('/settings'),
  update: (patch: SettingsUpdatePayload) => apiClient.put<SettingsOut>('/settings', patch),
  /**
   * 在线拉取某提供商的模型列表（GET /models，OpenAI 兼容协议）。
   * kind: 'llm' | 'embed'；baseUrl 为当前输入框的「预览地址」，未保存时后端不携带密钥。
   */
  providersModels: (kind: 'llm' | 'embed', providerId: string, baseUrl?: string) =>
    apiClient.get<ProviderModelsOut>(`/settings/providers/${kind}/${providerId}/models`, {
      params: { base_url: baseUrl || undefined },
    }),
}

export const documentsApi = {
  list: (category?: string) =>
    apiClient.get<DocumentListResponse>('/documents', { params: { category } }),
  upload: (
    file: File,
    category: string,
    onUploadProgress?: (percent: number) => void,
  ) => {
    const form = new FormData()
    form.append('file', file) // 字段名须匹配后端 UploadFile(...)
    form.append('category', category) // 字段名须匹配后端 Form(...)
    // 不手动设 Content-Type：axios 对 FormData 自动带 boundary
    return apiClient.post<UploadResponse>('/documents/upload', form, {
      onUploadProgress: (e) => {
        if (e.total) onUploadProgress?.(Math.round((e.loaded / e.total) * 100))
      },
    })
  },
  categories: () => apiClient.get<CategoryListResponse>('/documents/categories'),
  addCategory: (category: string) =>
    apiClient.post<CategoryListResponse>('/documents/categories', { category }),
  updateCategory: (docId: string, category: string) =>
    apiClient.patch<DocumentRecord>(`/documents/${docId}`, { category }),
  del: (docId: string) => apiClient.delete<void>(`/documents/${docId}`),
}

export const chatApi = {
  listSessions: () => apiClient.get<ChatSessionsResponse>('/chat/sessions'),
  messages: (sessionId: string) =>
    apiClient.get<ChatHistoryResponse>(`/chat/sessions/${sessionId}/messages`),
  query: (question: string, sessionId: string | null, category?: string | null) =>
    apiClient.post<QueryResponse>('/rag/query', {
      question,
      session_id: sessionId,
      category,
    }),
}

export const healthApi = {
  get: () => apiClient.get<HealthResponse>('/health'),
}

export const notesApi = {
  list: () => apiClient.get<NoteListResponse>('/notes'),
  get: (id: number) => apiClient.get<NoteOut>(`/notes/${id}`),
  create: (body: NoteCreate) => apiClient.post<NoteOut>('/notes', body),
  update: (id: number, body: NoteUpdate) => apiClient.patch<NoteOut>(`/notes/${id}`, body),
  del: (id: number) => apiClient.delete<void>(`/notes/${id}`),
  /** 「相关文档」推荐：用笔记正文临时检索知识库，不持久化 */
  related: (id: number) =>
    apiClient.get<RelatedDocumentListResponse>(`/notes/${id}/related-documents`),
  /** 自动分类并持久化标签；无 body */
  tags: (id: number) => apiClient.post<TagResponse>(`/notes/${id}/tags`),
}
