// 选中文本后的 AI 操作浮条（扩写 / 改写）。定位由 NoteEditor 用 coordsAtPos 计算（视口坐标）。

import { RefreshCw, WandSparkles } from 'lucide-react'

interface Props {
  left: number
  top: number
  onExpand: () => void
  onRewrite: () => void
}

export default function AssistFloatingBar({ left, top, onExpand, onRewrite }: Props) {
  return (
    <div
      className="fixed z-40 flex items-center gap-1 rounded-lg border border-border bg-panel px-1.5 py-1 shadow-pop"
      style={{ left, top: top - 44 }}
      onMouseDown={(e) => e.preventDefault() /* 保持编辑器选区，避免失焦收起 */}
    >
      <button
        type="button"
        className="flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium text-ink transition-colors duration-150 hover:bg-primary-weak hover:text-primary"
        onClick={onExpand}
      >
        <WandSparkles size={14} />
        扩写
      </button>
      <button
        type="button"
        className="flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium text-ink transition-colors duration-150 hover:bg-primary-weak hover:text-primary"
        onClick={onRewrite}
      >
        <RefreshCw size={14} />
        改写
      </button>
    </div>
  )
}
