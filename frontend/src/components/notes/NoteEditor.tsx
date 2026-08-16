// 笔记编辑器：Tiptap 富文本 + 防抖保存 + 自动分类 + 分类手动设置 + 相关文档推荐 + AI 辅助（SSE 流式插入）。
// 笔记完全独立；AI 辅助写作只基于笔记正文（不检索知识库）；知识库文档仅通过右侧「相关文档」面板间接出现（临时检索，不持久化）。

import { useEffect, useRef, useState } from 'react'
import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import {
  ArrowLeft,
  Bold,
  Check,
  ChevronDown,
  CircleX,
  Code,
  FileText,
  Heading1,
  Heading2,
  Heading3,
  Italic,
  List,
  ListOrdered,
  Loader2,
  PenLine,
  Quote,
  Redo,
  RefreshCw,
  Square,
  Tag,
  Undo,
  WandSparkles,
  X,
} from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { useAssistStream } from '@/hooks/useAssistStream'
import { upsertNote } from '@/hooks/notesStore'
import { notesApi } from '@/api/endpoints'
import { NOTE_TAGS } from '@/api/types'
import type { NoteOut, NoteUpdate, RelatedDocumentOut } from '@/api/types'
import { htmlLengthBefore } from '@/utils/html'
import AssistFloatingBar from './AssistFloatingBar'

type SaveState = 'idle' | 'dirty' | 'saving' | 'saved' | 'error'

interface Props {
  noteId: number
  onBack: () => void
}

export default function NoteEditor({ noteId, onBack }: Props) {
  const { openLoginModal } = useAuth()
  const { start, stop, generating } = useAssistStream()

  const [note, setNote] = useState<NoteOut | null>(null)
  const [loadError, setLoadError] = useState<string | null>(null)
  const [title, setTitle] = useState('')
  const [saveState, setSaveState] = useState<SaveState>('idle')
  const [tagging, setTagging] = useState(false)
  const [tagMenuOpen, setTagMenuOpen] = useState(false)
  const [assistError, setAssistError] = useState<string | null>(null)
  const [related, setRelated] = useState<RelatedDocumentOut[]>([])
  const [relatedLoading, setRelatedLoading] = useState(false)

  const [floatBar, setFloatBar] = useState<{
    left: number
    top: number
    from: number
    to: number
    text: string
  } | null>(null)

  // ---- 稳定引用（供定时器 / 异步闭包读取最新值） ----
  const noteRef = useRef<NoteOut | null>(null)
  const titleRef = useRef('')
  const contentReadyRef = useRef(false)
  const saveTimerRef = useRef<number | null>(null)
  const tagTimerRef = useRef<number | null>(null)
  const taggingRef = useRef(false)
  const dirtyRef = useRef(false)
  const insertRef = useRef<{ mode: 'continue' | 'replace'; pos: number; to: number; acc: number } | null>(null)

  useEffect(() => {
    titleRef.current = title
  }, [title])

  // ---- 加载笔记 + 相关文档推荐 ----
  const loadRelated = async () => {
    if (relatedLoading) return
    setRelatedLoading(true)
    try {
      const res = await notesApi.related(noteId)
      setRelated(res.data.related)
    } catch {
      /* 推荐失败静默，不阻塞编辑 */
    } finally {
      setRelatedLoading(false)
    }
  }

  useEffect(() => {
    let cancelled = false
    setLoadError(null)
    setNote(null)
    contentReadyRef.current = false
    void (async () => {
      try {
        const res = await notesApi.get(noteId)
        if (cancelled) return
        noteRef.current = res.data
        setNote(res.data)
        setTitle(res.data.title)
      } catch (e) {
        if (!cancelled) setLoadError((e as Error).message)
      }
      if (!cancelled) void loadRelated() // 用笔记正文临时检索知识库，纯展示
    })()
    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [noteId])

  // ---- 保存 ----
  const doSave = async () => {
    const n = noteRef.current
    if (!n) return
    dirtyRef.current = false
    setSaveState('saving')
    try {
      const res = await notesApi.update(n.id, {
        title: titleRef.current,
        content: editor?.getHTML() ?? n.content,
      })
      noteRef.current = res.data
      setNote(res.data)
      upsertNote(res.data)
      setSaveState('saved')
      void loadRelated() // 正文变更后刷新推荐
    } catch {
      dirtyRef.current = true
      setSaveState('error')
    }
  }

  const markDirty = () => {
    if (!noteRef.current) return
    dirtyRef.current = true
    setSaveState('dirty')
    if (saveTimerRef.current) window.clearTimeout(saveTimerRef.current)
    saveTimerRef.current = window.setTimeout(() => void doSave(), 800)
    // 停止编辑 4s 后自动分类（非阻塞）
    if (tagTimerRef.current) window.clearTimeout(tagTimerRef.current)
    tagTimerRef.current = window.setTimeout(() => void autoTag(), 4000)
  }

  // ---- 自动分类（AI 建议 + 持久化） ----
  const autoTag = async () => {
    const n = noteRef.current
    if (!n || taggingRef.current) return
    const content = editor?.getHTML() ?? ''
    if (!content.trim() && !titleRef.current.trim()) return
    taggingRef.current = true
    setTagging(true)
    try {
      const res = await notesApi.tags(n.id)
      const updated = { ...noteRef.current!, tag: res.data.tag }
      noteRef.current = updated
      setNote(updated)
      upsertNote(updated)
    } catch {
      /* 分类失败静默，不阻塞写作 */
    } finally {
      taggingRef.current = false
      setTagging(false)
    }
  }

  // ---- 手动设置分类（PATCH；清空分类需带 title 以通过「至少一个字段」校验） ----
  const setManualTag = async (tag: string | null) => {
    const n = noteRef.current
    if (!n) return
    setTagMenuOpen(false)
    try {
      // tag=null 会被 JSON.stringify 保留；后端「至少一个字段」校验需再带 title/content
      const body: { tag?: string | null; title?: string; content?: string } = { tag }
      if (tag === null) {
        body.title = n.title || undefined
        body.content = editor?.getHTML() ?? n.content
      }
      const res = await notesApi.update(n.id, body as NoteUpdate)
      noteRef.current = res.data
      setNote(res.data)
      upsertNote(res.data)
    } catch (e) {
      setAssistError((e as Error).message)
    }
  }

  // ---- Tiptap ----
  const editor = useEditor({
    extensions: [
      StarterKit.configure({ heading: { levels: [1, 2, 3] } }),
      Placeholder.configure({ placeholder: '开始书写…' }),
    ],
    content: '',
    onUpdate: () => markDirty(),
  })

  useEffect(() => {
    if (editor && note && !contentReadyRef.current) {
      editor.commands.setContent(note.content || '', { emitUpdate: false })
      contentReadyRef.current = true
    }
  }, [editor, note])

  // ---- 卸载前冲刷未保存内容（放在 useEditor 之后，避免依赖数组提前引用） ----
  useEffect(() => {
    return () => {
      if (saveTimerRef.current) window.clearTimeout(saveTimerRef.current)
      if (tagTimerRef.current) window.clearTimeout(tagTimerRef.current)
      if (dirtyRef.current && noteRef.current) {
        void notesApi
          .update(noteId, { title: titleRef.current, content: editor?.getHTML() ?? '' })
          .catch(() => {})
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [noteId, editor])

  // ---- 选中浮条：选中非空文本时弹出 扩写/改写 ----
  useEffect(() => {
    if (!editor) return
    const hide = () => setFloatBar(null)
    const onSelection = () => {
      const { empty, from, to } = editor.state.selection
      if (empty || generating || !editor.isFocused) {
        hide()
        return
      }
      const text = editor.state.doc.textBetween(from, to)
      if (!text.trim()) {
        hide()
        return
      }
      const coords = editor.view.coordsAtPos(from)
      setFloatBar({ left: coords.left, top: coords.top, from, to, text })
    }
    editor.on('selectionUpdate', onSelection)
    editor.on('blur', hide)
    return () => {
      editor.off('selectionUpdate', onSelection)
      editor.off('blur', hide)
    }
  }, [editor, generating])

  // ---- AI 辅助 ----
  const insertText = (text: string) => {
    const ins = insertRef.current
    if (!editor || !ins) return
    const target = ins.acc === 0 && ins.mode === 'replace' ? { from: ins.pos, to: ins.to } : ins.pos + ins.acc
    editor.chain().focus().insertContentAt(target, { type: 'text', text }).run()
    ins.acc += text.length
  }

  const doContinue = () => {
    if (!editor || generating || !noteRef.current) return
    const pos = editor.state.selection.$to.pos
    const atEnd = pos >= editor.state.doc.content.size
    const cursor_position = atEnd ? (noteRef.current.content.length || 0) : htmlLengthBefore(editor, pos)
    insertRef.current = { mode: 'continue', pos, to: pos, acc: 0 }
    setAssistError(null)
    void start(
      noteRef.current.id,
      { action: 'continue', cursor_position },
      {
        onToken: insertText,
        onDone: () => (insertRef.current = null),
        onError: (msg) => {
          insertRef.current = null
          setAssistError(msg)
        },
        onUnauthorized: openLoginModal,
      },
    )
  }

  const doExpandOrRewrite = (action: 'expand' | 'rewrite') => {
    if (!editor || generating || !noteRef.current || !floatBar) return
    insertRef.current = { mode: 'replace', pos: floatBar.from, to: floatBar.to, acc: 0 }
    setFloatBar(null)
    setAssistError(null)
    void start(
      noteRef.current.id,
      { action, selected_text: floatBar.text },
      {
        onToken: insertText,
        onDone: () => (insertRef.current = null),
        onError: (msg) => {
          insertRef.current = null
          setAssistError(msg)
        },
        onUnauthorized: openLoginModal,
      },
    )
  }

  if (loadError) {
    return (
      <div className="flex h-full items-center justify-center p-8">
        <div className="card max-w-sm p-8 text-center">
          <CircleX className="mx-auto mb-2 text-danger" size={28} />
          <p className="mb-4 text-sm text-muted">{loadError}</p>
          <button type="button" className="btn btn-primary" onClick={onBack}>
            <ArrowLeft size={14} /> 返回
          </button>
        </div>
      </div>
    )
  }

  if (!note) {
    return (
      <div className="flex h-full items-center justify-center gap-2 p-8 text-sm text-muted">
        <Loader2 size={16} className="animate-spin" /> 加载笔记…
      </div>
    )
  }

  return (
    <div className="flex h-full min-w-0">
      {/* 主编辑列 */}
      <div className="flex min-w-0 flex-1 flex-col">
        {/* 顶栏：返回 / 笔记标题 / 保存状态 */}
        <div className="flex items-center gap-2 border-b border-border px-6 py-3">
          <button
            type="button"
            onClick={onBack}
            aria-label="返回笔记列表"
            className="rounded-lg p-1.5 text-muted transition-colors duration-150 hover:bg-fill hover:text-ink"
          >
            <ArrowLeft size={16} />
          </button>
          <span className="truncate text-xs text-faint">{note.title}</span>
          <span className="ml-auto flex items-center gap-1 text-xs">
            {saveState === 'saving' && (
              <span className="flex items-center gap-1 text-faint">
                <Loader2 size={12} className="animate-spin" /> 保存中
              </span>
            )}
            {saveState === 'saved' && (
              <span className="flex items-center gap-1 text-ok">
                <Check size={12} /> 已保存
              </span>
            )}
            {saveState === 'dirty' && <span className="text-faint">未保存</span>}
            {saveState === 'error' && (
              <span className="flex items-center gap-1.5 text-danger">
                <CircleX size={12} /> 保存失败
                <button type="button" className="text-danger underline" onClick={() => void doSave()}>
                  重试
                </button>
              </span>
            )}
            {tagging && (
              <span className="flex items-center gap-1 text-faint">
                <Loader2 size={12} className="animate-spin" /> 分类中
              </span>
            )}
          </span>
        </div>

        {/* 标题 */}
        <input
          className="mx-6 mt-4 border-0 bg-transparent px-0 py-1 text-xl font-semibold text-ink outline-none placeholder:text-faint focus:ring-0"
          value={title}
          placeholder="笔记标题"
          onChange={(e) => {
            setTitle(e.target.value)
            markDirty()
          }}
        />

        {/* 工具条 */}
        <div className="flex flex-wrap items-center gap-1 border-b border-border px-6 py-2">
          <ToolBtn active={editor?.isActive('heading', { level: 1 })} title="一级标题" onClick={() => editor?.chain().focus().toggleHeading({ level: 1 }).run()}>
            <Heading1 size={16} />
          </ToolBtn>
          <ToolBtn active={editor?.isActive('heading', { level: 2 })} title="二级标题" onClick={() => editor?.chain().focus().toggleHeading({ level: 2 }).run()}>
            <Heading2 size={16} />
          </ToolBtn>
          <ToolBtn active={editor?.isActive('heading', { level: 3 })} title="三级标题" onClick={() => editor?.chain().focus().toggleHeading({ level: 3 }).run()}>
            <Heading3 size={16} />
          </ToolBtn>
          <Divider />
          <ToolBtn active={editor?.isActive('bold')} title="加粗" onClick={() => editor?.chain().focus().toggleBold().run()}>
            <Bold size={16} />
          </ToolBtn>
          <ToolBtn active={editor?.isActive('italic')} title="斜体" onClick={() => editor?.chain().focus().toggleItalic().run()}>
            <Italic size={16} />
          </ToolBtn>
          <Divider />
          <ToolBtn active={editor?.isActive('bulletList')} title="无序列表" onClick={() => editor?.chain().focus().toggleBulletList().run()}>
            <List size={16} />
          </ToolBtn>
          <ToolBtn active={editor?.isActive('orderedList')} title="有序列表" onClick={() => editor?.chain().focus().toggleOrderedList().run()}>
            <ListOrdered size={16} />
          </ToolBtn>
          <ToolBtn active={editor?.isActive('blockquote')} title="引用" onClick={() => editor?.chain().focus().toggleBlockquote().run()}>
            <Quote size={16} />
          </ToolBtn>
          <ToolBtn active={editor?.isActive('codeBlock')} title="代码块" onClick={() => editor?.chain().focus().toggleCodeBlock().run()}>
            <Code size={16} />
          </ToolBtn>
          <Divider />
          <ToolBtn title="撤销" onClick={() => editor?.chain().focus().undo().run()}>
            <Undo size={16} />
          </ToolBtn>
          <ToolBtn title="重做" onClick={() => editor?.chain().focus().redo().run()}>
            <Redo size={16} />
          </ToolBtn>

          <div className="ml-auto flex items-center gap-2">
            {generating ? (
              <>
                <span className="flex items-center gap-1.5 text-xs text-muted">
                  <Loader2 size={14} className="animate-spin" /> AI 生成中…
                </span>
                <button
                  type="button"
                  className="flex items-center gap-1.5 rounded-lg bg-danger px-3 py-1.5 text-xs font-medium text-white transition-colors duration-150 hover:opacity-90"
                  onClick={stop}
                >
                  <Square size={12} /> 停止
                </button>
              </>
            ) : (
              <button
                type="button"
                className="flex items-center gap-1.5 rounded-lg bg-primary px-3 py-1.5 text-xs font-medium text-white transition-colors duration-150 hover:bg-primary-strong"
                onClick={doContinue}
              >
                <PenLine size={12} /> 续写
              </button>
            )}
          </div>
        </div>

        {assistError && (
          <div className="flex items-center gap-2 border-b border-border bg-danger/10 px-6 py-2 text-xs text-danger">
            <CircleX size={13} />
            <span className="flex-1">{assistError}</span>
            <button
              type="button"
              aria-label="关闭提示"
              className="rounded p-0.5 text-danger transition-colors duration-150 hover:text-ink"
              onClick={() => setAssistError(null)}
            >
              <X size={13} />
            </button>
          </div>
        )}

        {/* 正文 */}
        <div className="flex-1 overflow-y-auto" onScroll={() => setFloatBar(null)}>
          <EditorContent
            editor={editor}
            className="mx-auto w-full max-w-3xl py-4 [&_.tiptap]:outline-none"
          />
        </div>

        {/* 元信息条 */}
        <div className="flex items-center gap-3 border-t border-border px-6 py-2.5 text-xs">
          {/* 分类 */}
          <div className="relative">
            <button
              type="button"
              onClick={() => setTagMenuOpen((o) => !o)}
              className="flex items-center gap-1.5 rounded-full border border-primary-line bg-primary-weak px-3 py-1 font-medium text-primary transition-colors duration-150 hover:bg-primary-weak/70"
            >
              <Tag size={12} />
              {note.tag ?? '未分类'}
              <ChevronDown size={12} />
            </button>
            {tagMenuOpen && (
              <>
                <div className="fixed inset-0 z-30" onClick={() => setTagMenuOpen(false)} />
                <div className="absolute bottom-full left-0 z-40 mb-1 w-32 rounded-lg border border-border bg-panel py-1 shadow-pop">
                  {NOTE_TAGS.map((t) => (
                    <button
                      key={t}
                      type="button"
                      className={`block w-full px-3 py-1.5 text-left transition-colors duration-150 hover:bg-fill ${
                        note.tag === t ? 'font-medium text-primary' : 'text-ink'
                      }`}
                      onClick={() => void setManualTag(t)}
                    >
                      {t}
                    </button>
                  ))}
                  {note.tag && (
                    <button
                      type="button"
                      className="block w-full px-3 py-1.5 text-left text-muted transition-colors duration-150 hover:bg-fill"
                      onClick={() => void setManualTag(null)}
                    >
                      无分类
                    </button>
                  )}
                </div>
              </>
            )}
          </div>
          <button
            type="button"
            className="flex items-center gap-1 rounded-full px-2.5 py-1 text-muted transition-colors duration-150 hover:bg-fill hover:text-ink"
            onClick={() => void autoTag()}
            disabled={tagging}
          >
            <WandSparkles size={12} />
            重新分类
          </button>
        </div>
      </div>

      {/* 相关文档推荐侧栏（临时检索，无硬关联、不可增删） */}
      <aside className="flex w-72 shrink-0 flex-col border-l border-border bg-panel">
        <div className="flex items-center justify-between border-b border-border px-4 py-3">
          <span className="text-sm font-medium text-ink">相关文档</span>
          <button
            type="button"
            aria-label="刷新推荐"
            title="刷新推荐"
            className="rounded p-1 text-faint transition-colors duration-150 hover:bg-fill hover:text-ink"
            onClick={() => void loadRelated()}
          >
            <RefreshCw size={13} className={relatedLoading ? 'animate-spin' : ''} />
          </button>
        </div>
        <div className="flex-1 space-y-2 overflow-y-auto p-3">
          {relatedLoading && related.length === 0 ? (
            <p className="flex items-center justify-center gap-1.5 py-6 text-xs text-faint">
              <Loader2 size={12} className="animate-spin" /> 检索中…
            </p>
          ) : related.length === 0 ? (
            <p className="py-6 text-center text-xs text-faint">
              根据笔记正文，暂无匹配的知识库文档。
            </p>
          ) : (
            related.map((d) => (
              <div key={d.doc_id} className="rounded-lg border border-border-weak p-3">
                <div className="flex items-start gap-2">
                  <FileText size={14} className="mt-0.5 shrink-0 text-faint" />
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-xs font-medium text-ink">{d.filename}</p>
                    <p className="mt-0.5 text-[10px] text-faint">
                      相关度 {Math.round(d.score * 100)}%
                      {d.chunk_count > 0 ? ` / ${d.chunk_count} 个片段` : ''}
                    </p>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </aside>

      {/* 选中浮条 */}
      {floatBar && (
        <AssistFloatingBar
          left={floatBar.left}
          top={floatBar.top}
          onExpand={() => void doExpandOrRewrite('expand')}
          onRewrite={() => void doExpandOrRewrite('rewrite')}
        />
      )}
    </div>
  )
}

function ToolBtn({
  active,
  title,
  onClick,
  children,
}: {
  active?: boolean
  title: string
  onClick: () => void
  children: React.ReactNode
}) {
  return (
    <button
      type="button"
      title={title}
      aria-label={title}
      onMouseDown={(e) => e.preventDefault()}
      onClick={onClick}
      className={`rounded-lg p-1.5 transition-colors duration-150 ${
        active ? 'bg-primary-weak text-primary' : 'text-muted hover:bg-fill hover:text-ink'
      }`}
    >
      {children}
    </button>
  )
}

function Divider() {
  return <span className="mx-1 h-4 w-px bg-border" />
}
