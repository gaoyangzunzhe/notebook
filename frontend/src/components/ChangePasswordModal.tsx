import { useState } from 'react'
import Modal from './Modal'
import PasswordField from './PasswordField'
import { authApi } from '@/api/endpoints'

/** 修改密码弹窗：旧 + 新 + 确认（客户端校验 ≥6 且一致，后端 400 映射为可读文案）。 */
export default function ChangePasswordModal({ onClose }: { onClose: () => void }) {
  const [oldPw, setOldPw] = useState('')
  const [newPw, setNewPw] = useState('')
  const [confirmPw, setConfirmPw] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    if (!oldPw) return setError('请输入当前密码')
    if (newPw.length < 6 || newPw.length > 72) return setError('新密码需 6–72 位')
    if (newPw !== confirmPw) return setError('两次输入的新密码不一致')
    setSubmitting(true)
    try {
      await authApi.changePassword(oldPw, newPw, confirmPw)
      onClose()
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Modal title="修改密码" onClose={onClose}>
      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <label className="text-sm text-muted">当前密码</label>
          <div className="mt-1">
            <PasswordField value={oldPw} onChange={setOldPw} placeholder="输入当前密码" autoFocus />
          </div>
        </div>
        <div>
          <label className="text-sm text-muted">新密码</label>
          <div className="mt-1">
            <PasswordField value={newPw} onChange={setNewPw} placeholder="6–72 位" />
          </div>
        </div>
        <div>
          <label className="text-sm text-muted">确认新密码</label>
          <div className="mt-1">
            <PasswordField value={confirmPw} onChange={setConfirmPw} placeholder="再次输入新密码" />
          </div>
        </div>
        {error && <p className="break-all text-sm text-danger">{error}</p>}
        <button type="submit" className="btn btn-primary w-full" disabled={submitting}>
          {submitting ? '提交中…' : '确认修改'}
        </button>
      </form>
    </Modal>
  )
}
