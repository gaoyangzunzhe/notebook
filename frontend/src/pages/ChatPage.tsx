import { useCallback, useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router'
import { ChevronDown, ChevronUp, MessageSquare } from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import {
  cacheMessages,
  getCachedMessages,
  refreshSessions,
  useSessions,
} from '@/hooks/sessionsStore'
import { chatApi, documentsApi } from '@/api/endpoints'
import type { ChatMessage } from '@/api/types'
import Spinner from '@/components/Spinner'

/** 「基于」选择器的全部文档哨兵值 */
const ALL_DOCS = '__all__'

export default function ChatPage() {
  const { status, openLoginModal } = useAuth()
  const { dbAvailable } = useSessions()
  const { sessionId } = useParams<{ sessionId?: string }>()
  const navigate = useNavigate()
  const authed = status === 'authed'
  // 首条消息的会话 id：发送成功前本地暂存，成功后再导航到 /chat/{id}
  const pendingId = useRef<string | null>(null)

  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [sending, setSending] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [input, setInput] = useState('')
  // 「基于」选择器：category=null 表示全部文档；每次新建对话（sessionId 缺失）重置为默认
  const [categories, setCategories] = useState<string[]>([])
  const [category, setCategory] = useState<string | null>(null)

  // 登录后拉取知识库分类（失败静默降级为空列表，退回全部文档）
  useEffect(() => {
    if (!authed) return
    let cancelled = false
    void documentsApi
      .categories()
      .then((res) => {
        if (!cancelled) setCategories(res.data.categories)
      })
      .catch(() => {})
    return () => {
      cancelled = true
    }
  }, [authed])

  // 新建对话（无 sessionId）→ 重置「基于」为默认全部文档
  useEffect(() => {
    if (!sessionId) setCategory(null)
  }, [sessionId])

  // /chat（无 sessionId）为空白新对话；有 sessionId 时载入该会话消息
  useEffect(() => {
    if (!authed || !sessionId) {
      setMessages([])
      return
    }
    let cancelled = false
    setError(null)
    const cached = getCachedMessages(sessionId)
    if (cached) {
      setMessages(cached)
      return
    }
    void (async () => {
      try {
        const res = await chatApi.messages(sessionId)
        if (cancelled) return
        const msgs: ChatMessage[] = res.data.messages.map((m) => ({ ...m }))
        setMessages(msgs)
        cacheMessages(sessionId, msgs)
      } catch {
        if (cancelled) return
        setMessages([]) // 会话尚无记录：视为空
      }
    })()
    return () => {
      cancelled = true
    }
  }, [authed, sessionId])

  const send = useCallback(async () => {
    const q = input.trim()
    if (!q || sending) return
    setInput('')
    setError(null)
    // 无 session 时先本地生成 id，发送成功后才导航；期间所有写缓存都用 sid
    const sid = sessionId ?? pendingId.current ?? (pendingId.current = crypto.randomUUID())
    const userMsg: ChatMessage = {
      id: -Date.now(),
      role: 'user',
      content: q,
      created_at: new Date().toISOString(),
    }
    const pending: ChatMessage = {
      id: -Date.now() - 1,
      role: 'assistant',
      content: '',
      created_at: new Date().toISOString(),
      pending: true,
    }
    const optimistic = [...messages, userMsg, pending]
    setMessages(optimistic)
    cacheMessages(sid, optimistic)
    setSending(true)
    try {
      const res = await chatApi.query(q, sid, category)
      const ans: ChatMessage = {
        id: -Date.now() - 2,
        role: 'assistant',
        content: res.data.answer,
        created_at: new Date().toISOString(),
        sources: res.data.sources,
      }
      const done = [...messages, userMsg, ans]
      setMessages(done)
      // 先缓存再导航：路由切换后消息 effect 直接从缓存取，不闪空、不重复请求
      cacheMessages(sid, done)
      if (pendingId.current === sid) {
        navigate(`/chat/${sid}`, { replace: true })
        pendingId.current = null
      }
      // 会话列表刷新出真实条目（首条消息后才建会话）
      void refreshSessions()
    } catch (e) {
      const msg = (e as Error).message
      const rollback = messages.filter((m) => m.id !== userMsg.id && !m.pending)
      setMessages(rollback)
      cacheMessages(sid, rollback)
      setInput(q) // 失败恢复输入，不丢内容
      setError(msg)
    } finally {
      setSending(false)
    }
  }, [input, sending, sessionId, messages, navigate, category])

  if (!authed) {
    return (
      <div className="flex h-full items-center justify-center p-8">
        <div className="card max-w-sm p-8 text-center">
          <MessageSquare className="mx-auto mb-2 text-primary" size={28} />
          <p className="mb-2 text-lg font-semibold">对话</p>
          <p className="mb-4 text-sm text-muted">登录后开始与知识库对话。</p>
          <button type="button" className="btn btn-primary" onClick={openLoginModal}>
            点击登录
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-full flex-col">
      <header className="border-b border-border px-6 py-3">
        <h1 className="text-base font-semibold">对话</h1>
      </header>

      {!dbAvailable && (
        <div className="bg-danger/10 px-6 py-2 text-xs text-danger">
          数据库未配置：会话不会保存，仅当前页面可见。
        </div>
      )}

      <div className="flex-1 space-y-4 overflow-y-auto px-6 py-4">
        {messages.length === 0 ? (
          <div className="flex h-full items-center justify-center text-sm text-muted">
            还没有对话。先在知识库上传文档，再回到这里提问。
          </div>
        ) : (
          messages.map((m) => <Bubble key={m.id} m={m} />)
        )}
      </div>

      {error && <p className="px-6 pb-2 text-sm text-danger">{error}</p>}

      <div className="border-t border-border px-6 py-3">
        <form
          onSubmit={(e) => {
            e.preventDefault()
            void send()
          }}
          className="flex gap-2"
        >
          <label className="flex shrink-0 items-center gap-1.5 text-sm text-muted" htmlFor="chat-based-on">
            基于
          </label>
          <select
            id="chat-based-on"
            className="shrink-0 rounded-lg border border-border bg-panel px-2 py-2 text-sm text-ink focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
            value={category ?? ALL_DOCS}
            onChange={(e) => setCategory(e.target.value === ALL_DOCS ? null : e.target.value)}
          >
            <option value={ALL_DOCS}>全部文档</option>
            {categories.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
          <input
            className="input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="输入问题，回车发送…"
            disabled={sending}
          />
          <button
            type="submit"
            className="btn btn-primary shrink-0"
            disabled={sending || !input.trim()}
          >
            {sending ? <Spinner /> : '发送'}
          </button>
        </form>
      </div>
    </div>
  )
}

function Bubble({ m }: { m: ChatMessage }) {
  const [open, setOpen] = useState(false)

  if (m.role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="max-w-[70%] whitespace-pre-wrap break-words rounded-card bg-primary px-4 py-2 text-sm text-white">
          {m.content}
        </div>
      </div>
    )
  }

  if (m.pending) {
    return (
      <div className="flex justify-start">
        <div className="flex items-center gap-2 rounded-card border border-border bg-panel px-4 py-2 text-sm text-muted">
          <Spinner /> 思考中…
        </div>
      </div>
    )
  }

  return (
    <div className="flex justify-start">
      <div className="max-w-[80%]">
        <div className="whitespace-pre-wrap break-words rounded-card border border-border bg-panel px-4 py-2 text-sm text-ink">
          {m.content}
        </div>
        {m.sources && m.sources.length > 0 && (
          <div className="mt-1">
            <button
              type="button"
              className="flex items-center gap-1 text-xs text-primary"
              onClick={() => setOpen((o) => !o)}
            >
              参考来源（{m.sources.length}）
              {open ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>
            {open && (
              <div className="mt-1 space-y-1">
                {m.sources.map((s, i) => (
                  <div key={i} className="rounded-md border border-border bg-bg p-2">
                    <p className="text-xs text-muted">
                      {s.source} · {s.score.toFixed(4)}
                    </p>
                    <p className="mt-0.5 text-xs text-ink line-clamp-3">{s.text}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
