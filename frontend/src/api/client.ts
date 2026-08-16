import axios, { type AxiosError, type AxiosRequestConfig } from 'axios'

const TOKEN_KEY = 'nb_token'

let accessToken: string | null = localStorage.getItem(TOKEN_KEY)

export const getAccessToken = (): string | null => accessToken

export const setAccessToken = (t: string | null): void => {
  accessToken = t
  if (t) localStorage.setItem(TOKEN_KEY, t)
  else localStorage.removeItem(TOKEN_KEY)
}

// 只走相对路径 /api/v1，dev 时由 Vite 代理转发到后端
export const apiClient = axios.create({
  baseURL: '/api/v1',
  timeout: 120_000, // RAG 生成较慢，放宽超时
})

// ---- 401 登录 gating：首个 401 弹登录框，其余并发 401 等待同一 gate ----
// 登录/注册/me 自身不触发弹窗（否则注册→登录自动序列会死锁）
const SKIP_MODAL = [/\/auth\/(login|register|me)$/]

let authGate: Promise<void> | null = null
let resolveGate: (() => void) | null = null
let rejectGate: ((e: unknown) => void) | null = null
let openLoginModal: () => void = () => {}

/** 由 AuthContext 挂载：任何请求 401 时的弹窗入口 */
export function setOpenLoginModal(fn: () => void): void {
  openLoginModal = fn
}

/** 登录成功：放行所有排队请求，原请求带新 token 自动重放 */
export function resolveAuthGate(): void {
  resolveGate?.()
  authGate = null
  resolveGate = null
  rejectGate = null
}

/** 取消弹窗 / 退出登录：排队请求以「请先登录」报错，不悬挂 */
export function rejectAuthGate(): void {
  rejectGate?.(new Error('请先登录'))
  authGate = null
  resolveGate = null
  rejectGate = null
}

apiClient.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }
  return config
})

apiClient.interceptors.response.use(
  (res) => res,
  async (error: AxiosError<{ detail?: unknown }>) => {
    const status = error.response?.status
    const url = error.config?.url ?? ''
    const config = error.config as (AxiosRequestConfig & { _retried?: boolean }) | undefined

    // 401 且非登录类端点、且未重放过：进入登录 gating
    if (status === 401 && config && !config._retried && !SKIP_MODAL.some((re) => re.test(url))) {
      if (!authGate) {
        authGate = new Promise<void>((res, rej) => {
          resolveGate = res
          rejectGate = rej
        })
        openLoginModal() // 只弹一次（单飞）
      }
      try {
        await authGate
        // 登录成功后带新 token 重放原请求
        return await apiClient.request({ ...config, _retried: true } as AxiosRequestConfig & {
          _retried?: boolean
        })
      } catch (e) {
        return Promise.reject(e)
      }
    }

    // 后端错误统一返回 { detail }，这里转成可读错误
    const detail: unknown = error.response?.data?.detail
    const message =
      typeof detail === 'string' ? detail : error.message ?? '网络错误，请确认后端已启动'
    return Promise.reject(new Error(message))
  },
)
