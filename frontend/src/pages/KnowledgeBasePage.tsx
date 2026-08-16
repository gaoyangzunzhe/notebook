import { useCallback, useEffect, useRef, useState } from 'react'
import { CircleCheck, CircleX, FolderPlus, Upload } from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { useDocuments } from '@/hooks/useDocuments'
import { documentsApi } from '@/api/endpoints'
import ConfirmDialog from '@/components/ConfirmDialog'
import Pill from '@/components/Pill'
import Spinner from '@/components/Spinner'
import { formatDateTime } from '@/utils/format'
import { isSupportedFile } from '@/utils/constants'

interface UploadItem {
  key: string
  file: File
  status: 'pending' | 'uploading' | 'done' | 'error'
  progress: number
  message?: string
  chunkCount?: number
}

let uid = 0

export default function KnowledgeBasePage() {
  const { status, openLoginModal } = useAuth()
  const { documents, loading, error, dbAvailable, refresh, deleteOne } = useDocuments()
  const [items, setItems] = useState<UploadItem[]>([])
  const [dragging, setDragging] = useState(false)
  const [confirmId, setConfirmId] = useState<string | null>(null)
  const [deleting, setDeleting] = useState(false)
  const [delError, setDelError] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  // ---- 分类相关 ----
  const [categories, setCategories] = useState<string[]>(['未分类'])
  const [filterCategory, setFilterCategory] = useState<string | null>(null)
  const [uploadCategory, setUploadCategory] = useState('未分类')
  const [newCat, setNewCat] = useState('')
  const [catError, setCatError] = useState<string | null>(null)
  const [editingId, setEditingId] = useState<string | null>(null) // 正在内联改分类的 doc_id
  const [editingValue, setEditingValue] = useState('')
  const editingOriginalRef = useRef('')
  const catInputRef = useRef<HTMLInputElement>(null)

  const authed = status === 'authed'

  const loadCategories = useCallback(async () => {
    try {
      const res = await documentsApi.categories()
      setCategories(res.data.categories)
    } catch {
      /* 分类加载失败静默，保留兜底 未分类 */
    }
  }, [])

  // 登录后拉取文档列表与分类
  useEffect(() => {
    if (!authed) return
    void refresh()
    void loadCategories()
  }, [authed, refresh, loadCategories])

  // window 级防拖拽：拖到区域外不触发浏览器跳转
  useEffect(() => {
    const prevent = (e: DragEvent) => e.preventDefault()
    window.addEventListener('dragover', prevent)
    window.addEventListener('drop', prevent)
    return () => {
      window.removeEventListener('dragover', prevent)
      window.removeEventListener('drop', prevent)
    }
  }, [])

  const uploadAll = useCallback(
    async (list: UploadItem[]) => {
      for (const item of list) {
        if (item.status === 'error') continue
        setItems((prev) =>
          prev.map((it) => (it.key === item.key ? { ...it, status: 'uploading' as const } : it)),
        )
        try {
          const res = await documentsApi.upload(item.file, uploadCategory, (p) => {
            setItems((prev) =>
              prev.map((it) => (it.key === item.key ? { ...it, progress: p } : it)),
            )
          })
          setItems((prev) =>
            prev.map((it) =>
              it.key === item.key
                ? { ...it, status: 'done' as const, progress: 100, chunkCount: res.data.chunk_count }
                : it,
            ),
          )
          await refresh() // 以服务端为准刷新列表
          void loadCategories() // 新分类可能因此出现（并集）
        } catch (e) {
          setItems((prev) =>
            prev.map((it) =>
              it.key === item.key
                ? { ...it, status: 'error' as const, message: (e as Error).message }
                : it,
            ),
          )
        }
      }
    },
    [refresh, loadCategories, uploadCategory],
  )

  const handleFiles = useCallback(
    (files: FileList | File[]) => {
      if (!authed) {
        openLoginModal()
        return
      }
      const added: UploadItem[] = []
      for (const f of Array.from(files)) {
        if (f.type === '') continue // 忽略目录
        const supported = isSupportedFile(f.name)
        added.push({
          key: `${f.name}-${f.size}-${uid++}`,
          file: f,
          status: supported ? 'pending' : 'error',
          progress: 0,
          message: supported ? undefined : '不支持的格式',
        })
      }
      if (added.length === 0) return
      const next = [...items, ...added]
      setItems(next)
      void uploadAll(next)
    },
    [authed, openLoginModal, items, uploadAll],
  )

  // ---- 新建分类 ----
  const handleAddCategory = async () => {
    const name = newCat.trim()
    if (!name || catError) return
    setCatError(null)
    try {
      await documentsApi.addCategory(name)
      await loadCategories()
      setNewCat('')
    } catch (e) {
      setCatError((e as Error).message)
    }
  }

  // ---- 内联改分类（Enter 保存 / Esc 取消） ----
  const startEdit = (docId: string, current: string) => {
    setEditingId(docId)
    setEditingValue(current)
    editingOriginalRef.current = current
  }
  const commitEdit = async (docId: string) => {
    const next = editingValue.trim()
    setEditingId(null)
    if (!next || next === editingOriginalRef.current) return // 未变更则跳过
    try {
      await documentsApi.updateCategory(docId, next)
      await refresh()
      await loadCategories()
    } catch (e) {
      setCatError((e as Error).message)
    }
  }

  const handleDelete = async (docId: string) => {
    setDeleting(true)
    setDelError(null)
    try {
      await deleteOne(docId)
      setConfirmId(null)
      await loadCategories()
    } catch (e) {
      const msg = (e as Error).message
      if (msg.includes('不存在')) {
        await refresh() // 已被并发删除，拉最新
        setConfirmId(null)
      } else {
        setDelError(msg)
      }
    } finally {
      setDeleting(false)
    }
  }

  // 分类筛选（客户端过滤，上传/删除后无需感知筛选态）
  const visible = filterCategory
    ? documents.filter((d) => d.category === filterCategory)
    : documents

  return (
    <div className="mx-auto max-w-4xl p-8">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-xl font-semibold">知识库</h1>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => (authed ? inputRef.current?.click() : openLoginModal())}
        >
          <Upload size={16} />
          上传文档
        </button>
      </div>

      {/* 分类筛选 pills + 新建分类 */}
      <div className="mb-4 flex flex-wrap items-center gap-2">
        <Pill active={filterCategory === null} onClick={() => setFilterCategory(null)}>
          全部
        </Pill>
        {categories.map((c) => (
          <Pill key={c} active={filterCategory === c} onClick={() => setFilterCategory(c)}>
            {c}
          </Pill>
        ))}
        <span className="mx-1 h-4 w-px bg-border" />
        <input
          className="w-36 rounded-full border border-border bg-panel px-3 py-1.5 text-sm text-ink placeholder:text-faint focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
          placeholder="新建分类…"
          value={newCat}
          maxLength={50}
          onChange={(e) => setNewCat(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') void handleAddCategory()
            if (e.key === 'Escape') setNewCat('')
          }}
        />
        <button
          type="button"
          className="btn btn-ghost px-2.5 py-1.5 text-sm"
          disabled={!newCat.trim()}
          onClick={() => void handleAddCategory()}
          title="回车确认"
        >
          <FolderPlus size={14} />
          新建分类
        </button>
      </div>
      {catError && <p className="mb-3 text-sm text-danger">{catError}</p>}

      {/* 拖拽上传区 */}
      <div
        className={`flex flex-col items-center justify-center rounded-card border-2 border-dashed px-6 py-8 text-center transition-colors ${
          dragging ? 'border-primary bg-primary-weak' : 'border-border'
        }`}
        onDragOver={(e) => {
          e.preventDefault()
          setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault()
          setDragging(false)
          handleFiles(e.dataTransfer.files)
        }}
      >
        <p className="text-sm text-muted">拖拽文件到此处，或点击「上传文档」</p>
        <p className="mt-1 text-xs text-muted">支持：.txt .md .markdown .pdf .docx .pptx</p>
        {/* 上传分类：可输入 combobox（含已有分类 + 自由输入） */}
        <div className="mt-3 flex items-center gap-2">
          <label className="text-xs text-muted" htmlFor="upload-category">
            归入分类
          </label>
          <input
            id="upload-category"
            list="doc-categories"
            className="w-40 rounded-lg border border-border bg-panel px-3 py-1.5 text-sm text-ink placeholder:text-faint focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
            value={uploadCategory}
            maxLength={50}
            onChange={(e) => setUploadCategory(e.target.value)}
          />
          <datalist id="doc-categories">
            {categories.map((c) => (
              <option key={c} value={c} />
            ))}
          </datalist>
        </div>
        <input
          ref={inputRef}
          type="file"
          multiple
          accept=".txt,.md,.markdown,.pdf,.docx,.pptx"
          className="hidden"
          onChange={(e) => {
            if (e.target.files) handleFiles(e.target.files)
            e.target.value = '' // 清空以便重复选择同一文件
          }}
        />
      </div>

      {/* 上传状态 */}
      {items.length > 0 && (
        <div className="mt-4 space-y-2">
          {items.map((it) => (
            <div key={it.key} className="card flex items-center gap-3 px-4 py-2.5 text-sm">
              <span className="flex-1 truncate">{it.file.name}</span>
              {it.status === 'uploading' && (
                <>
                  <Spinner />
                  <span className="text-xs text-muted">{it.progress}% · 处理中…</span>
                </>
              )}
              {it.status === 'pending' && <span className="text-xs text-muted">等待上传…</span>}
              {it.status === 'done' && (
                <span className="flex items-center gap-1 text-xs text-ok">
                  <CircleCheck size={14} /> 已入库（{it.chunkCount} 块）
                </span>
              )}
              {it.status === 'error' && (
                <span className="flex items-center gap-1 text-xs text-danger">
                  <CircleX size={14} /> {it.message ?? '失败'}
                </span>
              )}
            </div>
          ))}
        </div>
      )}

      {/* 文档列表 */}
      <div className="mt-6">
        {!dbAvailable && (
          <p className="mb-3 rounded-lg bg-danger/10 px-4 py-2 text-xs text-danger">
            数据库未配置：文档列表不会保存，仅供本次会话查看。
          </p>
        )}
        {error && <p className="mb-3 text-sm text-danger">{error}</p>}
        {loading ? (
          <div className="flex justify-center py-10">
            <Spinner />
          </div>
        ) : documents.length === 0 ? (
          <p className="py-10 text-center text-sm text-muted">还没有文档，上传第一个吧。</p>
        ) : visible.length === 0 ? (
          <p className="py-10 text-center text-sm text-muted">该分类下暂无文档。</p>
        ) : (
          <div className="card divide-y divide-border overflow-hidden">
            {visible.map((d) => (
              <div key={d.doc_id} className="flex items-center gap-3 px-4 py-3 text-sm">
                <span className="flex-1 truncate font-medium text-ink">{d.filename}</span>
                {editingId === d.doc_id ? (
                  <input
                    ref={catInputRef}
                    autoFocus
                    list="doc-categories"
                    className="w-32 rounded-lg border border-primary bg-panel px-2 py-1 text-xs text-ink focus:outline-none focus:ring-2 focus:ring-primary/20"
                    value={editingValue}
                    maxLength={50}
                    onChange={(e) => setEditingValue(e.target.value)}
                    onBlur={() => void commitEdit(d.doc_id)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        e.preventDefault()
                        void commitEdit(d.doc_id)
                      }
                      if (e.key === 'Escape') setEditingId(null)
                    }}
                  />
                ) : (
                  <button
                    type="button"
                    title="点击修改分类"
                    className="max-w-28 truncate rounded-full border border-primary-line bg-primary-weak px-2.5 py-0.5 text-xs font-medium text-primary transition-colors duration-150 hover:bg-primary-weak/70"
                    onClick={() => startEdit(d.doc_id, d.category)}
                  >
                    {d.category}
                  </button>
                )}
                <span className="text-xs text-muted">{d.chunk_count} 块</span>
                <span className="text-xs text-muted">{formatDateTime(d.created_at)}</span>
                <button
                  type="button"
                  className="btn btn-ghost px-2 py-1 text-xs text-danger hover:bg-danger/10"
                  onClick={() => setConfirmId(d.doc_id)}
                >
                  删除
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {delError && <p className="mt-2 text-sm text-danger">{delError}</p>}

      {confirmId && (
        <ConfirmDialog
          title="删除文档"
          message={`确定删除「${
            documents.find((d) => d.doc_id === confirmId)?.filename ?? confirmId
          }」？其向量块将一并移除。`}
          onCancel={() => setConfirmId(null)}
          onConfirm={() => void handleDelete(confirmId)}
          loading={deleting}
        />
      )}
    </div>
  )
}
