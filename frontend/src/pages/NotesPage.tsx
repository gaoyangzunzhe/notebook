// 笔记页（URL 驱动：?note=笔记）
// 列表视图：顶部栏（标题 + 新建笔记）+ 搜索 + 分类筛选 pill + 笔记卡片
// 编辑器视图：?note= 存在时渲染 NoteEditor
// 笔记完全独立：不归属笔记本、不选择分类（分类由 AI 建议 + 手动修改，固定五类）

import { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router'
import { Loader2, NotebookPen, Plus, Search } from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { refreshNotes, upsertNote, useNotes } from '@/hooks/notesStore'
import { notesApi } from '@/api/endpoints'
import { NOTE_TAGS } from '@/api/types'
import type { NoteOut } from '@/api/types'
import { htmlToText } from '@/utils/html'
import NoteCard from '@/components/notes/NoteCard'
import NoteEditor from '@/components/notes/NoteEditor'
import Pill from '@/components/Pill'

const NONE_TAG = '__none__'

export default function NotesPage() {
  const { status, openLoginModal } = useAuth()
  const authed = status === 'authed'

  const { notes, loading } = useNotes()
  const [params, setParams] = useSearchParams()

  // 缺参时 params.get() 返回 null，Number(null)=0 会误判成「id=0」→ 须先判空
  const noteId = parseIdParam(params.get('note'))

  const [search, setSearch] = useState('')
  const [filterTag, setFilterTag] = useState<string | null>(null)
  const [listError, setListError] = useState<string | null>(null)

  // 登录后拉取全部笔记
  useEffect(() => {
    if (!authed) return
    void refreshNotes()
  }, [authed])

  // 过滤逻辑必须放在所有早期 return（未登录 / 编辑器视图）之前，
  // 否则切到编辑器渲染时会少调用一个 hook，报 Rendered fewer hooks。
  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase()
    return notes.filter((n: NoteOut) => {
      if (filterTag === NONE_TAG) {
        if (n.tag !== null) return false
      } else if (filterTag && n.tag !== filterTag) {
        return false
      }
      if (q) {
        const title = n.title.toLowerCase()
        const body = htmlToText(n.content).toLowerCase()
        if (!title.includes(q) && !body.includes(q)) return false
      }
      return true
    })
  }, [notes, search, filterTag])

  if (!authed) {
    return (
      <div className="flex h-full items-center justify-center p-8">
        <div className="card max-w-sm p-8 text-center">
          <NotebookPen className="mx-auto mb-2 text-primary" size={28} />
          <p className="mb-2 text-lg font-semibold">笔记</p>
          <p className="mb-4 text-sm text-muted">登录后开始记录你的笔记，AI 辅助写作。</p>
          <button type="button" className="btn btn-primary" onClick={openLoginModal}>
            点击登录
          </button>
        </div>
      </div>
    )
  }

  // ---- 编辑器视图 ----
  if (noteId !== null) {
    return (
      <NoteEditor
        key={noteId}
        noteId={noteId}
        onBack={() => setParams({})}
      />
    )
  }

  // ---- 列表视图 ----
  const createNote = async () => {
    setListError(null)
    try {
      const res = await notesApi.create({ title: '未命名笔记' })
      upsertNote(res.data) // 即时入库，返回列表不依赖刷新时机
      void refreshNotes() // 后台对账（seq 保护，旧响应丢弃）
      setParams({ note: String(res.data.id) })
    } catch (e) {
      setListError((e as Error).message)
    }
  }

  return (
    <div className="mx-auto flex h-full max-w-5xl flex-col px-8 py-8">
      {/* 顶部栏 */}
      <div className="mb-6 flex items-center justify-between gap-3">
        <h1 className="text-2xl font-bold text-ink">笔记</h1>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => void createNote()}
        >
          <Plus size={14} />
          新建笔记
        </button>
      </div>

      {/* 搜索 */}
      <div className="relative mb-6">
        <Search
          size={16}
          className="absolute left-3 top-1/2 w-4 -translate-y-1/2 text-faint"
        />
        <input
          className="w-full rounded-xl border border-border bg-panel py-2.5 pl-10 pr-4 text-sm text-ink placeholder:text-faint focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
          placeholder="搜索标题或正文…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* 分类筛选 */}
      <div className="mb-6 flex flex-wrap gap-2">
        <Pill active={filterTag === null} onClick={() => setFilterTag(null)}>
          全部
        </Pill>
        {NOTE_TAGS.map((t) => (
          <Pill key={t} active={filterTag === t} onClick={() => setFilterTag(t)}>
            {t}
          </Pill>
        ))}
        <Pill active={filterTag === NONE_TAG} onClick={() => setFilterTag(NONE_TAG)}>
          未分类
        </Pill>
      </div>

      {listError && <p className="mb-4 text-sm text-danger">{listError}</p>}

      {/* 内容区 */}
      <div className="flex-1 overflow-y-auto pb-4">
        {loading && notes.length === 0 ? (
          <div className="flex items-center justify-center gap-2 py-16 text-muted">
            <Loader2 size={18} className="animate-spin" /> 加载中…
          </div>
        ) : notes.length === 0 ? (
          <div className="card mx-auto mt-8 max-w-sm p-10 text-center">
            <NotebookPen className="mx-auto mb-3 text-primary" size={32} />
            <p className="mb-1 text-base font-semibold">还没有笔记</p>
            <p className="mb-5 text-sm text-muted">点击右上角「新建笔记」开始记录。</p>
            <button type="button" className="btn btn-primary" onClick={() => void createNote()}>
              <Plus size={14} />
              新建笔记
            </button>
          </div>
        ) : filtered.length === 0 ? (
          <div className="card mx-auto mt-8 max-w-sm p-10 text-center">
            <p className="mb-1 text-base font-semibold">没有匹配的笔记</p>
            <p className="mb-5 text-sm text-muted">试试调整搜索词或筛选条件。</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {filtered.map((n) => (
              <NoteCard
                key={n.id}
                note={n}
                onClick={() => setParams({ note: String(n.id) })}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

/** 解析 ?note= 数字参数；缺参/非法 → null（避免 Number(null)=0 误判） */
function parseIdParam(raw: string | null): number | null {
  if (raw === null || raw === '') return null
  const n = Number(raw)
  return Number.isFinite(n) && n > 0 ? n : null
}
