import { useEffect, useRef, useState } from 'react'
import { NavLink, useLocation, useNavigate, useParams } from 'react-router'
import { BookOpen, Library, MessageSquare, NotebookPen, Plus } from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { usePreferences } from '@/context/PreferencesContext'
import { useSessions } from '@/hooks/sessionsStore'
import Avatar from '@/components/Avatar'
import UserMenu from '@/components/UserMenu'
import AboutModal from '@/components/AboutModal'
import { relativeTime } from '@/utils/format'

export default function Sidebar() {
  const { status, user, openLoginModal } = useAuth()
  const { sidebarCollapsed, update } = usePreferences()
  const { sessions, refresh } = useSessions()
  const navigate = useNavigate()
  const { pathname } = useLocation()
  const { sessionId } = useParams<{ sessionId?: string }>()
  const [chatOpen, setChatOpen] = useState(pathname.startsWith('/chat'))
  const [menuOpen, setMenuOpen] = useState(false)
  const [showAbout, setShowAbout] = useState(false)
  const menuTimer = useRef<number | null>(null)

  const authed = status === 'authed'

  // 登录后拉取会话列表；导航离开 /chat 时收起会话列表
  useEffect(() => {
    if (authed) void refresh()
  }, [authed, refresh])

  useEffect(() => {
    if (!pathname.startsWith('/chat')) setChatOpen(false)
  }, [pathname])

  const toggleChat = () => {
    if (sidebarCollapsed) update({ sidebarCollapsed: false })
    setChatOpen((o) => !o)
  }

  const openSession = (id: string) => navigate(`/chat/${id}`)

  const newChat = () => navigate('/chat')

  const showMenu = () => {
    if (menuTimer.current) window.clearTimeout(menuTimer.current)
    setMenuOpen(true)
  }
  const hideMenu = () => {
    if (menuTimer.current) window.clearTimeout(menuTimer.current)
    menuTimer.current = window.setTimeout(() => setMenuOpen(false), 150)
  }

  const navClass = (isActive: boolean) =>
    `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors duration-150 ${
      isActive
        ? 'bg-primary-weak text-primary'
        : 'text-muted hover:bg-fill hover:text-ink'
    }`

  return (
    <aside
      className={`flex h-full shrink-0 flex-col border-r border-border bg-panel transition-[width] duration-200 ${
        sidebarCollapsed ? 'w-16' : 'w-56'
      }`}
    >
      {/* 品牌 */}
      <div className="flex items-center gap-2 px-5 py-4 text-lg font-bold text-ink">
        <BookOpen size={20} className="shrink-0 text-primary" />
        {!sidebarCollapsed && <span>智能笔记</span>}
      </div>

      {/* 导航 */}
      <nav className="flex-1 space-y-1 overflow-y-auto px-3">
        <NavLink to="/notes" className={({ isActive }) => navClass(isActive)}>
          <NotebookPen size={18} className="w-5 shrink-0" />
          {!sidebarCollapsed && <span>笔记</span>}
        </NavLink>
        <NavLink to="/kb" className={({ isActive }) => navClass(isActive)}>
          <Library size={18} className="w-5 shrink-0" />
          {!sidebarCollapsed && <span>知识库</span>}
        </NavLink>
        <NavLink to="/chat" className={({ isActive }) => navClass(isActive)} onClick={toggleChat}>
          <MessageSquare size={18} className="w-5 shrink-0" />
          {!sidebarCollapsed && <span>对话</span>}
        </NavLink>

        {/* 对话可展开的会话列表：顶部固定「新对话」，下面只列服务端真实会话 */}
        {chatOpen && !sidebarCollapsed && (
          <div className="mb-1 space-y-0.5 border-l border-border pb-1 pl-2">
            {!authed ? (
              <button
                type="button"
                onClick={openLoginModal}
                className="w-full px-2 py-1.5 text-left text-xs text-muted hover:text-ink"
              >
                点击登录后查看对话
              </button>
            ) : (
              <>
                <button
                  type="button"
                  onClick={newChat}
                  className="flex w-full items-center gap-1.5 rounded-md px-2 py-1.5 text-left text-xs font-medium text-primary hover:bg-primary-weak"
                >
                  <Plus size={14} />
                  新对话
                </button>
                {sessions.map((s) => (
                  <SessionItem
                    key={s.session_id}
                    title={s.title}
                    time={s.updated_at}
                    count={s.message_count}
                    active={sessionId === s.session_id}
                    onClick={() => openSession(s.session_id)}
                  />
                ))}
              </>
            )}
          </div>
        )}
      </nav>

      {/* 用户区 */}
      <div
        className="relative border-t border-border p-3"
        onMouseEnter={showMenu}
        onMouseLeave={hideMenu}
      >
        {menuOpen && authed && (
          <UserMenu
            onClose={() => setMenuOpen(false)}
            onOpenAbout={() => setShowAbout(true)}
          />
        )}
        {user ? (
          <div className="flex items-center gap-2.5">
            <Avatar name={user.username} src={user.avatar} size={32} />
            {!sidebarCollapsed && <span className="truncate text-sm text-ink">{user.username}</span>}
          </div>
        ) : (
          <button type="button" className="btn btn-ghost w-full text-xs" onClick={openLoginModal}>
            点击登录
          </button>
        )}
      </div>

      {/* 关于弹窗：挂在 Sidebar 上，避免随用户菜单（menuOpen 条件渲染）一起卸载 */}
      {showAbout && <AboutModal onClose={() => setShowAbout(false)} />}
    </aside>
  )
}

function SessionItem({
  title,
  time,
  count,
  active,
  onClick,
}: {
  title: string
  time: string
  count: number
  active: boolean
  onClick: () => void
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`block w-full rounded-md px-2 py-1.5 text-left text-xs ${
        active
          ? 'bg-primary-weak text-primary'
          : 'text-muted hover:bg-primary-weak hover:text-ink'
      }`}
    >
      <span className="block truncate font-medium">{title}</span>
      <span className="block text-[10px] opacity-70">
        {count} 条 · {time ? relativeTime(time) : ''}
      </span>
    </button>
  )
}
