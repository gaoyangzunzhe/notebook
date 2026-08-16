// 共享筛选 pill：NotesPage 与 KnowledgeBasePage 共用（分类筛选）。
import type { ReactNode } from 'react'

export default function Pill({
  active,
  onClick,
  children,
}: {
  active: boolean
  onClick: () => void
  children: ReactNode
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors duration-150 ${
        active ? 'bg-primary text-white' : 'bg-fill text-muted hover:bg-border'
      }`}
    >
      {children}
    </button>
  )
}
