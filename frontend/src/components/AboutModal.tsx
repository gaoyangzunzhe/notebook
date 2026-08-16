import { BookOpen } from 'lucide-react'
import Modal from './Modal'
import { useHealth } from '@/hooks/useHealth'

const STACK = [
  'React 19 / Vite 6 / TypeScript / Tailwind CSS 4',
  'FastAPI / SQLAlchemy 2 (async) / PostgreSQL',
  'LangChain / Chroma 向量库',
  '自定义对话模型 / 自定义嵌入模型',
]

export default function AboutModal({ onClose }: { onClose: () => void }) {
  const health = useHealth()
  return (
    <Modal title="关于我们" onClose={onClose}>
      <div className="space-y-3 text-sm text-ink">
        <p className="flex items-center gap-2 text-base font-semibold">
          <BookOpen size={18} className="text-primary" /> 智能笔记
        </p>
        <p className="text-muted">以人为主、AI 为辅的笔记 + 知识库问答应用。</p>
        <ul className="list-disc space-y-1 pl-5 text-muted">
          {STACK.map((s) => (
            <li key={s}>{s}</li>
          ))}
        </ul>
        <p className="text-xs text-muted">版本：{health?.version ?? 'dev'}</p>
      </div>
      <div className="mt-5 flex justify-end">
        <button type="button" className="btn btn-ghost" onClick={onClose}>
          关闭
        </button>
      </div>
    </Modal>
  )
}
