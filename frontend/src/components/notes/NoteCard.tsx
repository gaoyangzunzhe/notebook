// 笔记卡片：标题 / 更新时间 / 正文预览 / 标签 pill。点击打开编辑器。

import type { NoteOut } from '@/api/types'
import { relativeTime } from '@/utils/format'
import { htmlToText } from '@/utils/html'

interface Props {
  note: NoteOut
  onClick: () => void
}

export default function NoteCard({ note, onClick }: Props) {
  const preview = htmlToText(note.content) || '（空笔记）'
  return (
    <button
      type="button"
      onClick={onClick}
      className="block w-full rounded-2xl border border-border-weak bg-panel p-5 text-left shadow-card transition-all duration-150 hover:border-border hover:shadow-md"
    >
      <div className="mb-2 flex items-start justify-between gap-3">
        <span className="line-clamp-1 text-base font-semibold text-ink">
          {note.title || '未命名笔记'}
        </span>
        <span className="shrink-0 text-xs text-faint">{relativeTime(note.updated_at)}</span>
      </div>
      <p className="mb-4 line-clamp-2 text-sm leading-relaxed text-muted">{preview}</p>
      <div className="flex flex-wrap gap-2">
        {note.tag ? (
          <span className="rounded-full border border-primary-line bg-primary-weak px-2.5 py-1 text-xs font-medium text-primary">
            {note.tag}
          </span>
        ) : (
          <span className="rounded-full bg-fill px-2.5 py-1 text-xs font-medium text-muted">未分类</span>
        )}
      </div>
    </button>
  )
}
