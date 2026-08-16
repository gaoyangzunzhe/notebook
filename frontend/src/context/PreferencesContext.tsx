import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react'
import { settingsApi } from '@/api/endpoints'
import { useAuth } from '@/context/AuthContext'

const PREFS_KEY = 'nb_prefs'

export type ThemeMode = 'light' | 'dark' | 'system'

export interface Preferences {
  theme: ThemeMode
  sidebarCollapsed: boolean
}

export const DEFAULT_PREFS: Preferences = {
  theme: 'system',
  sidebarCollapsed: false,
}

interface PreferencesContextValue extends Preferences {
  update: (patch: Partial<Preferences>) => void
}

const PreferencesContext = createContext<PreferencesContextValue | null>(null)

function loadPrefs(): Preferences {
  try {
    const raw = localStorage.getItem(PREFS_KEY)
    if (!raw) return DEFAULT_PREFS
    return { ...DEFAULT_PREFS, ...JSON.parse(raw) }
  } catch {
    return DEFAULT_PREFS
  }
}

function prefersSystemDark(): boolean {
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

export function PreferencesProvider({ children }: { children: React.ReactNode }) {
  const { status } = useAuth()
  const authed = status === 'authed'
  const [prefs, setPrefs] = useState<Preferences>(loadPrefs)
  const [systemDark, setSystemDark] = useState(prefersSystemDark)
  const syncTimer = useRef<number | null>(null)
  // 始终引用最新 prefs，供防抖回调读取，避免闭包过期
  const prefsRef = useRef(prefs)
  prefsRef.current = prefs

  // 跟随系统配色：订阅 matchMedia，theme=system 时生效
  useEffect(() => {
    const mq = window.matchMedia('(prefers-color-scheme: dark)')
    const onChange = (e: MediaQueryListEvent) => setSystemDark(e.matches)
    mq.addEventListener('change', onChange)
    return () => mq.removeEventListener('change', onChange)
  }, [])

  // 应用主题：html.dark 类 + color-scheme（暗色变量在 index.css 的 .dark 块覆盖）
  useEffect(() => {
    const effectiveDark =
      prefs.theme === 'dark' || (prefs.theme === 'system' && systemDark)
    document.documentElement.classList.toggle('dark', effectiveDark)
  }, [prefs.theme, systemDark])

  // 登录后拉取 user_settings.ui：有服务端值则以服务端为准（跨设备一致），否则保留本地
  useEffect(() => {
    if (!authed) return
    let cancelled = false
    settingsApi
      .get()
      .then((res) => {
        if (cancelled) return
        const ui = res.data.ui
        if (ui.theme === null && ui.sidebar_collapsed === null) return
        setPrefs((prev) => {
          const next: Preferences = {
            theme: (ui.theme as ThemeMode | null) ?? prev.theme,
            sidebarCollapsed: ui.sidebar_collapsed ?? prev.sidebarCollapsed,
          }
          localStorage.setItem(PREFS_KEY, JSON.stringify(next))
          return next
        })
      })
      .catch(() => {
        /* 拉取失败沿用本地 */
      })
    return () => {
      cancelled = true
    }
  }, [authed])

  // 卸载时清理防抖定时器
  useEffect(
    () => () => {
      if (syncTimer.current) window.clearTimeout(syncTimer.current)
    },
    [],
  )

  const update = (patch: Partial<Preferences>) => {
    setPrefs((prev) => {
      const next = { ...prev, ...patch }
      localStorage.setItem(PREFS_KEY, JSON.stringify(next))
      return next
    })
    // 登录后把 UI 偏好防抖同步到 user_settings（fire-and-forget）
    if (authed) {
      if (syncTimer.current) window.clearTimeout(syncTimer.current)
      syncTimer.current = window.setTimeout(() => {
        const latest = prefsRef.current
        settingsApi
          .update({ ui: { theme: latest.theme, sidebar_collapsed: latest.sidebarCollapsed } })
          .catch(() => {
            /* 同步失败静默，下轮再试 */
          })
      }, 500)
    }
  }

  const value = useMemo<PreferencesContextValue>(() => ({ ...prefs, update }), [prefs, update])
  return <PreferencesContext.Provider value={value}>{children}</PreferencesContext.Provider>
}

export function usePreferences(): PreferencesContextValue {
  const ctx = useContext(PreferencesContext)
  if (!ctx) throw new Error('usePreferences must be used within PreferencesProvider')
  return ctx
}
