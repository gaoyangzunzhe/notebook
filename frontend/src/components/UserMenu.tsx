import { useNavigate } from 'react-router'
import { useAuth } from '@/context/AuthContext'

export default function UserMenu({
  onClose,
  onOpenAbout,
}: {
  onClose: () => void
  onOpenAbout: () => void
}) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const item = 'w-full px-4 py-2 text-left text-sm text-ink hover:bg-primary-weak'

  const go = (path: string) => {
    onClose()
    navigate(path)
  }

  return (
    <div className="absolute bottom-full left-0 z-40 mb-2 w-44 overflow-hidden rounded-card border border-border bg-panel shadow-lg">
      {user && (
        <div className="border-b border-border px-4 py-2 text-xs text-muted">
          {user.username}
        </div>
      )}
      <button type="button" className={item} onClick={() => go('/settings')}>
        设置
      </button>
      <button
        type="button"
        className={item}
        onClick={() => {
          onClose()
          onOpenAbout()
        }}
      >
        关于我们
      </button>
      <button
        type="button"
        className={`${item} text-danger hover:bg-danger/10`}
        onClick={() => {
          onClose()
          logout()
        }}
      >
        退出登录
      </button>
    </div>
  )
}
