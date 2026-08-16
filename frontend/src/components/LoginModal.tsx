import { useState } from 'react'
import Modal from './Modal'
import PasswordField from './PasswordField'
import { useAuth } from '@/context/AuthContext'

const USERNAME_RE = /^[A-Za-z0-9_]{3,20}$/
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export default function LoginModal() {
  const { loginModalOpen, closeLoginModal, login, register } = useAuth()
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [account, setAccount] = useState('')
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  if (!loginModalOpen) return null

  const switchMode = (m: 'login' | 'register') => {
    setMode(m)
    setPassword('')
    setConfirm('')
    setError(null)
  }

  const validate = (): string | null => {
    if (mode === 'register') {
      const u = username.trim()
      if (!USERNAME_RE.test(u)) return '用户名需 3–20 位字母/数字/下划线'
      if (!EMAIL_RE.test(email.trim())) return '请输入正确的邮箱地址'
      if (password.length < 6 || password.length > 72) return '密码需 6–72 位'
      if (password !== confirm) return '两次输入的密码不一致'
    } else {
      if (!account.trim()) return '请输入用户名或邮箱'
      if (!password) return '请输入密码'
    }
    return null
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const v = validate()
    if (v) {
      setError(v)
      return
    }
    setSubmitting(true)
    setError(null)
    try {
      if (mode === 'login') {
        await login(account.trim(), password)
      } else {
        await register(username.trim(), email.trim(), password, confirm)
      }
      // 成功后由 AuthContext resolveAuthGate，排队请求自动重放
      setAccount('')
      setUsername('')
      setEmail('')
      setPassword('')
      setConfirm('')
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Modal title={mode === 'login' ? '登录' : '注册'} onClose={closeLoginModal}>
      <div className="mb-4 flex gap-1 rounded-lg bg-bg p-1">
        <button
          type="button"
          className={mode === 'login' ? 'btn btn-primary flex-1' : 'btn btn-ghost flex-1'}
          onClick={() => switchMode('login')}
        >
          登录
        </button>
        <button
          type="button"
          className={mode === 'register' ? 'btn btn-primary flex-1' : 'btn btn-ghost flex-1'}
          onClick={() => switchMode('register')}
        >
          注册
        </button>
      </div>
      <form onSubmit={handleSubmit} className="space-y-3">
        {mode === 'login' ? (
          <div>
            <label className="text-sm text-muted">账号（用户名或邮箱）</label>
            <input
              className="input mt-1"
              value={account}
              onChange={(e) => setAccount(e.target.value)}
              placeholder="用户名或邮箱"
              autoFocus
            />
          </div>
        ) : (
          <>
            <div>
              <label className="text-sm text-muted">用户名</label>
              <input
                className="input mt-1"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="3–20 位字母/数字/下划线"
                autoFocus
              />
            </div>
            <div>
              <label className="text-sm text-muted">邮箱</label>
              <input
                className="input mt-1"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
              />
            </div>
          </>
        )}
        <div>
          <label className="text-sm text-muted">密码</label>
          <div className="mt-1">
            <PasswordField
              value={password}
              onChange={setPassword}
              placeholder={mode === 'register' ? '6–72 位' : '输入密码'}
            />
          </div>
        </div>
        {mode === 'register' && (
          <div>
            <label className="text-sm text-muted">确认密码</label>
            <div className="mt-1">
              <PasswordField value={confirm} onChange={setConfirm} placeholder="再次输入密码" />
            </div>
          </div>
        )}
        {error && <p className="break-all text-sm text-danger">{error}</p>}
        <button type="submit" className="btn btn-primary w-full" disabled={submitting}>
          {submitting ? '请稍候…' : mode === 'login' ? '登录' : '注册并登录'}
        </button>
      </form>
    </Modal>
  )
}
