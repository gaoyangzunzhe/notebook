import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react'
import { authApi } from '@/api/endpoints'
import {
  getAccessToken,
  rejectAuthGate,
  resolveAuthGate,
  setAccessToken,
  setOpenLoginModal,
} from '@/api/client'
import type { User } from '@/api/types'

type AuthStatus = 'idle' | 'loading' | 'authed' | 'unauthed'

interface AuthContextValue {
  user: User | null
  status: AuthStatus
  loginModalOpen: boolean
  openLoginModal: () => void
  closeLoginModal: () => void
  login: (account: string, password: string) => Promise<void>
  register: (
    username: string,
    email: string,
    password: string,
    confirmPassword: string,
  ) => Promise<void>
  logout: () => void
  updateUser: (user: User) => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

// 用户身份本地副本：登录后写入，供未登录/首屏即显（与 nb_token 的 JWT 信息互补）
const USER_KEY = 'nb_user'

function persistUser(user: User): void {
  try {
    localStorage.setItem(USER_KEY, JSON.stringify({ id: user.id, username: user.username, email: user.email }))
  } catch {
    /* 忽略 localStorage 不可用 */
  }
}

function clearPersistedUser(): void {
  localStorage.removeItem(USER_KEY)
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [status, setStatus] = useState<AuthStatus>('idle')
  const [loginModalOpen, setLoginModalOpen] = useState(false)

  const openLoginModal = useCallback(() => setLoginModalOpen(true), [])

  // 关闭弹窗时若有挂起 gate（排队请求），以「请先登录」拒绝，避免悬挂
  const closeLoginModal = useCallback(() => {
    rejectAuthGate()
    setLoginModalOpen(false)
  }, [])

  // 挂载 openLoginModal 到 api/client，供 401 拦截器触发
  useEffect(() => {
    setOpenLoginModal(openLoginModal)
  }, [openLoginModal])

  // 启动恢复会话：有 token 则静默校验 /auth/me；401 清除 token 不弹窗
  useEffect(() => {
    let cancelled = false
    const token = getAccessToken()
    if (!token) {
      setStatus('unauthed')
      return
    }
    setStatus('loading')
    authApi
      .me()
      .then((res) => {
        if (cancelled) return
        setUser(res.data)
        persistUser(res.data)
        setStatus('authed')
      })
      .catch(() => {
        if (cancelled) return
        setAccessToken(null)
        setUser(null)
        clearPersistedUser()
        setStatus('unauthed')
      })
    return () => {
      cancelled = true
    }
  }, [])

  const login = useCallback(async (account: string, password: string) => {
    const res = await authApi.login(account, password)
    setAccessToken(res.data.access_token)
    const me = await authApi.me()
    setUser(me.data)
    persistUser(me.data)
    setStatus('authed')
    resolveAuthGate() // 放行排队请求（原请求带新 token 自动重放）
    setLoginModalOpen(false)
  }, [])

  const register = useCallback(
    async (username: string, email: string, password: string, confirmPassword: string) => {
      // register 返回 UserOut（无 token），必须再显式登录
      await authApi.register(username, email, password, confirmPassword)
      await login(username, password)
    },
    [login],
  )

  const logout = useCallback(() => {
    setAccessToken(null)
    setUser(null)
    clearPersistedUser()
    setStatus('unauthed')
    rejectAuthGate()
    setLoginModalOpen(false)
  }, [])

  // 设置页改用户名 / 换头像后回写最新用户信息
  const updateUser = useCallback((next: User) => {
    setUser(next)
    persistUser(next)
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      status,
      loginModalOpen,
      openLoginModal,
      closeLoginModal,
      login,
      register,
      logout,
      updateUser,
    }),
    [user, status, loginModalOpen, openLoginModal, closeLoginModal, login, register, logout, updateUser],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
