import { useCallback, useEffect, useRef, useState } from 'react'
import { BookOpen, Camera, KeyRound, Trash2 } from 'lucide-react'
import { authApi, settingsApi } from '@/api/endpoints'
import type { SettingsOut, User } from '@/api/types'
import { useAuth } from '@/context/AuthContext'
import { usePreferences, type ThemeMode } from '@/context/PreferencesContext'
import { useHealth } from '@/hooks/useHealth'
import Avatar from '@/components/Avatar'
import ToggleSwitch from '@/components/ToggleSwitch'
import PasswordField from '@/components/PasswordField'
import ModelPicker from '@/components/ModelPicker'
import ChangePasswordModal from '@/components/ChangePasswordModal'
import { formatDateTime } from '@/utils/format'

const STACK = [
  'React 19 / Vite 6 / TypeScript / Tailwind CSS 4',
  'FastAPI / SQLAlchemy 2 (async) / PostgreSQL',
  'LangChain / Chroma 向量库',
  '自定义对话模型 / 自定义嵌入模型',
]

const USERNAME_RE = /^[A-Za-z0-9_]{3,20}$/

// 知识库卡片的后端全局默认（缺省展示位）
const KB_DEFAULTS = { top_k: 4, chunk_size: 1000, similarity_threshold: 0 }

type SaveState = { saving: boolean; msg: string | null; err: string | null }

const IDLE: SaveState = { saving: false, msg: null, err: null }

export default function SettingsPage() {
  const { user, status, openLoginModal, updateUser } = useAuth()
  const prefs = usePreferences()
  const health = useHealth()
  const authed = status === 'authed'

  // 服务端设置（AI / 知识库；外观偏好走 PreferencesContext）
  const [settings, setSettings] = useState<SettingsOut | null>(null)

  // AI 模型表单
  const [provider, setProvider] = useState('')
  const [model, setModel] = useState('')
  const [llmBaseUrl, setLlmBaseUrl] = useState('') // 自定义接口地址（网关/代理）；空 = 提供商默认
  const [apiKey, setApiKey] = useState('')
  const [clearKey, setClearKey] = useState(false)
  const [temperature, setTemperature] = useState(0.2)
  const [llmSave, setLlmSave] = useState<SaveState>(IDLE)
  // 在线拉取的模型列表：null = 未拉到，用注册表建议列表兜底
  const [llmModels, setLlmModels] = useState<string[] | null>(null)
  const [llmFetching, setLlmFetching] = useState(false)
  const [llmFetchNote, setLlmFetchNote] = useState<string | null>(null)

  // 知识库表单
  const [topK, setTopK] = useState(KB_DEFAULTS.top_k)
  const [chunkSize, setChunkSize] = useState(KB_DEFAULTS.chunk_size)
  const [threshold, setThreshold] = useState(KB_DEFAULTS.similarity_threshold)
  const [embedProvider, setEmbedProvider] = useState('')
  const [embedModel, setEmbedModel] = useState('')
  const [embedBaseUrl, setEmbedBaseUrl] = useState('')
  const [embedApiKey, setEmbedApiKey] = useState('')
  const [embedClearKey, setEmbedClearKey] = useState(false)
  const [kbSave, setKbSave] = useState<SaveState>(IDLE)
  const [embedModels, setEmbedModels] = useState<string[] | null>(null)
  const [embedFetching, setEmbedFetching] = useState(false)
  const [embedFetchNote, setEmbedFetchNote] = useState<string | null>(null)

  // 个人信息表单
  const [username, setUsername] = useState('')
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null)
  const [avatarFile, setAvatarFile] = useState<File | null>(null)
  const avatarInputRef = useRef<HTMLInputElement>(null)
  const [profileSave, setProfileSave] = useState<SaveState>(IDLE)
  const [showPwModal, setShowPwModal] = useState(false)

  // 拉取用户级设置
  useEffect(() => {
    if (!authed) return
    let cancelled = false
    setSettings(null)
    settingsApi
      .get()
      .then((res) => {
        if (!cancelled) setSettings(res.data)
      })
      .catch(() => {
        /* 读取失败保持空表单 */
      })
    return () => {
      cancelled = true
    }
  }, [authed])

  // 设置到位后填充表单（llm 用 stored 覆盖值 ?? effective 生效值）
  useEffect(() => {
    if (!settings) return
    const llm = settings.llm
    const eff = llm.effective
    const p = llm.provider ?? eff?.provider ?? ''
    setProvider(p)
    const info = settings.providers.find((x) => x.id === p)
    setModel(llm.model ?? eff?.model ?? info?.models[0] ?? '')
    setLlmBaseUrl(llm.base_url ?? '')
    setTemperature(llm.temperature ?? eff?.temperature ?? 0.2)
    setApiKey('')
    setClearKey(false)

    const kb = settings.kb
    const emb = kb.embed
    const embEff = emb.effective
    const ep = emb.provider ?? embEff.provider ?? ''
    setEmbedProvider(ep)
    const eInfo = settings.embed_providers.find((x) => x.id === ep)
    setEmbedModel(emb.model ?? embEff.model ?? eInfo?.models[0] ?? '')
    setEmbedBaseUrl(emb.base_url ?? '')
    setEmbedApiKey('')
    setEmbedClearKey(false)
    setTopK(kb.top_k ?? kb.effective.top_k ?? KB_DEFAULTS.top_k)
    setChunkSize(kb.chunk_size ?? kb.effective.chunk_size ?? KB_DEFAULTS.chunk_size)
    setThreshold(
      kb.similarity_threshold ?? kb.effective.similarity_threshold ?? KB_DEFAULTS.similarity_threshold,
    )
  }, [settings])

  useEffect(() => {
    if (user) setUsername(user.username)
  }, [user])

  // AI 模型卡派生状态：生效配置 / 是否用户覆盖 / 模型下拉选项
  const llm = settings?.llm
  const eff = llm?.effective
  const hasOverride = !!(
    llm &&
    (llm.provider != null || llm.temperature != null || llm.api_key_set || llm.base_url != null)
  )
  const keyConfigured = !!(llm?.api_key_set || eff?.api_key_set)
  const providerInfo = settings?.providers.find((p) => p.id === provider)
  // 在线拉取的模型优先；未拉到用注册表建议列表
  const modelOptions = llmModels ?? providerInfo?.models ?? []

  // 嵌入模型卡派生状态：生效配置 / 是否用户覆盖 / 建议模型
  const emb = settings?.kb.embed
  const embEff = emb?.effective
  const embedHasOverride = !!(
    emb &&
    (emb.provider != null || emb.api_key_set || emb.base_url != null)
  )
  const embedKeyConfigured = !!(emb?.api_key_set || embEff?.api_key_set)
  const embedProviderInfo = settings?.embed_providers.find(
    (p) => p.id === embedProvider,
  )
  const embedModelOptions = embedModels ?? embedProviderInfo?.models ?? []

  // 提供商/设置变化时在线拉取模型列表（GET /models，参考 LibreChat models.fetch）。
  // 不依赖 llmBaseUrl：避免每次输入地址都触发请求，保存成功后 settings 变化会重新拉取。
  useEffect(() => {
    setLlmModels(null)
    setLlmFetchNote(null)
    if (!authed || !settings || !provider) return
    let cancelled = false
    setLlmFetching(true)
    settingsApi
      .providersModels('llm', provider, llmBaseUrl.trim() || undefined)
      .then((res) => {
        if (cancelled) return
        setLlmModels(res.data.models.length ? res.data.models : null)
        setLlmFetchNote(res.data.note)
      })
      .catch(() => {
        if (cancelled) return
        setLlmModels(null)
        setLlmFetchNote('在线拉取失败，使用建议列表')
      })
      .finally(() => {
        if (!cancelled) setLlmFetching(false)
      })
    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [authed, settings, provider])

  useEffect(() => {
    setEmbedModels(null)
    setEmbedFetchNote(null)
    if (!authed || !settings || !embedProvider) return
    let cancelled = false
    setEmbedFetching(true)
    settingsApi
      .providersModels('embed', embedProvider, embedBaseUrl.trim() || undefined)
      .then((res) => {
        if (cancelled) return
        setEmbedModels(res.data.models.length ? res.data.models : null)
        setEmbedFetchNote(res.data.note)
      })
      .catch(() => {
        if (cancelled) return
        setEmbedModels(null)
        setEmbedFetchNote('在线拉取失败，使用建议列表')
      })
      .finally(() => {
        if (!cancelled) setEmbedFetching(false)
      })
    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [authed, settings, embedProvider])

  const onProviderChange = (p: string) => {
    setProvider(p)
    const info = settings?.providers.find((x) => x.id === p)
    setModel(info?.models[0] ?? '')
  }

  const onEmbedProviderChange = (p: string) => {
    setEmbedProvider(p)
    const info = settings?.embed_providers.find((x) => x.id === p)
    setEmbedModel(info?.models[0] ?? '')
  }

  const saveLlm = async () => {
    if (!settings) return
    const s = settings.llm
    const e = s.effective
    // 未检测到实际改动（含跟随默认时未动任何字段）就不发 PUT，避免把 env 默认值固化成用户覆盖
    const changed =
      clearKey ||
      !!apiKey ||
      provider !== (s.provider ?? e?.provider ?? '') ||
      model !== (s.model ?? e?.model ?? '') ||
      llmBaseUrl.trim() !== (s.base_url ?? '') ||
      Math.abs(temperature - (s.temperature ?? e?.temperature ?? 0.2)) > 1e-9
    if (!changed) {
      setLlmSave({ saving: false, msg: null, err: '未检测到改动' })
      return
    }
    setLlmSave({ ...IDLE, saving: true })
    const patch: Parameters<typeof settingsApi.update>[0] = {
      llm: {
        provider: provider || null,
        base_url: llmBaseUrl.trim() || null,
        model: provider ? model || undefined : undefined,
        api_key: clearKey ? '' : apiKey || undefined,
        temperature,
      },
    }
    try {
      const res = await settingsApi.update(patch)
      setSettings(res.data)
      setLlmSave({ saving: false, msg: '已保存', err: null })
    } catch (err) {
      setLlmSave({ saving: false, msg: null, err: (err as Error).message })
    }
  }

  const restoreLlmDefault = async () => {
    if (!settings) return
    setLlmSave({ ...IDLE, saving: true })
    try {
      // provider=null 连带清 model/base_url/key；temperature=null 清温度覆盖 -> 全部回退 .env
      const res = await settingsApi.update({
        llm: {
          provider: null,
          model: null,
          base_url: null,
          api_key: '',
          temperature: null,
        },
      })
      setSettings(res.data)
      setLlmSave({ saving: false, msg: '已恢复系统默认', err: null })
    } catch (err) {
      setLlmSave({ saving: false, msg: null, err: (err as Error).message })
    }
  }

  const saveKb = async () => {
    if (!settings) return
    const kb = settings.kb
    const b = kb.effective
    // 未检测到实际改动就不发 PUT（避免把 env 默认值固化成用户覆盖）
    const changed =
      embedClearKey ||
      !!embedApiKey ||
      topK !== (kb.top_k ?? b.top_k ?? KB_DEFAULTS.top_k) ||
      chunkSize !== (kb.chunk_size ?? b.chunk_size ?? KB_DEFAULTS.chunk_size) ||
      threshold !==
        (kb.similarity_threshold ?? b.similarity_threshold ?? KB_DEFAULTS.similarity_threshold) ||
      embedProvider !== (kb.embed.provider ?? kb.embed.effective.provider ?? '') ||
      embedModel !== (kb.embed.model ?? kb.embed.effective.model ?? '') ||
      embedBaseUrl.trim() !== (kb.embed.base_url ?? '')
    if (!changed) {
      setKbSave({ saving: false, msg: null, err: '未检测到改动' })
      return
    }
    setKbSave({ ...IDLE, saving: true })
    try {
      const res = await settingsApi.update({
        kb: {
          top_k: topK,
          chunk_size: chunkSize,
          similarity_threshold: threshold,
          embed: {
            provider: embedProvider || null,
            base_url: embedBaseUrl.trim() || null,
            model: embedProvider ? embedModel || undefined : undefined,
            api_key: embedClearKey ? '' : embedApiKey || undefined,
          },
        },
      })
      setSettings(res.data)
      setKbSave({ saving: false, msg: '已保存', err: null })
    } catch (err) {
      setKbSave({ saving: false, msg: null, err: (err as Error).message })
    }
  }

  const restoreKbDefault = async () => {
    if (!settings) return
    setKbSave({ ...IDLE, saving: true })
    try {
      // 标量与嵌入 provider/base_url 全置 null -> 完全回退 .env / 系统默认
      const res = await settingsApi.update({
        kb: {
          top_k: null,
          chunk_size: null,
          similarity_threshold: null,
          embed: { provider: null, model: null, base_url: null, api_key: '' },
        },
      })
      setSettings(res.data)
      setKbSave({ saving: false, msg: '已恢复系统默认', err: null })
    } catch (err) {
      setKbSave({ saving: false, msg: null, err: (err as Error).message })
    }
  }

  const onAvatarPick = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    setAvatarFile(file)
    const reader = new FileReader()
    reader.onload = () => setAvatarPreview(reader.result as string)
    reader.readAsDataURL(file)
    e.target.value = '' // 允许重复选择同一文件
  }

  const saveAvatar = async () => {
    if (!avatarFile) return
    setProfileSave({ ...IDLE, saving: true })
    try {
      const res = await authApi.uploadAvatar(avatarFile)
      updateUser(res.data)
      setAvatarPreview(null)
      setAvatarFile(null)
      setProfileSave({ saving: false, msg: '头像已更新', err: null })
    } catch (err) {
      setProfileSave({ saving: false, msg: null, err: (err as Error).message })
    }
  }

  const removeAvatar = async () => {
    setProfileSave({ ...IDLE, saving: true })
    try {
      await authApi.deleteAvatar()
      updateUser({ ...(user as User), avatar: null })
      setAvatarPreview(null)
      setAvatarFile(null)
      setProfileSave({ saving: false, msg: '头像已移除', err: null })
    } catch (err) {
      setProfileSave({ saving: false, msg: null, err: (err as Error).message })
    }
  }

  const saveUsername = async () => {
    const u = username.trim()
    if (!USERNAME_RE.test(u)) {
      setProfileSave({ saving: false, msg: null, err: '用户名需 3–20 位字母/数字/下划线' })
      return
    }
    setProfileSave({ ...IDLE, saving: true })
    try {
      const res = await authApi.updateUsername(u)
      updateUser(res.data)
      setProfileSave({ saving: false, msg: '用户名已更新', err: null })
    } catch (err) {
      setProfileSave({ saving: false, msg: null, err: (err as Error).message })
    }
  }

  const displayAvatar = avatarPreview ?? user?.avatar ?? null

  return (
    <div className="mx-auto max-w-2xl space-y-6 p-8">
      <h1 className="text-xl font-semibold">设置</h1>

      {/* AI 模型 */}
      <section className="card p-6">
        <h2 className="mb-4 text-base font-semibold">AI 模型</h2>
        {!authed ? (
          <p className="text-sm text-muted">
            登录后可配置自己的大模型。
            <button type="button" className="ml-2 text-primary" onClick={openLoginModal}>
              点击登录
            </button>
          </p>
        ) : settings ? (
          <div className="space-y-4 text-sm">
            {eff?.warning && (
              <p className="rounded-lg bg-danger/10 px-3 py-2 text-xs leading-relaxed text-danger">
                {eff.warning}
              </p>
            )}
            <div>
              <label className="text-muted">提供商</label>
              <select
                className="input mt-1"
                value={provider}
                onChange={(e) => onProviderChange(e.target.value)}
              >
                {!provider && <option value="">请选择提供商</option>}
                {settings.providers.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name}
                  </option>
                ))}
              </select>
              {!hasOverride && eff && (
                <p className="mt-1 text-xs text-faint">
                  未自定义，当前使用系统默认：
                  {settings.providers.find((p) => p.id === eff.provider)?.name ??
                    eff.base_url}{' '}
                  / {eff.model ?? ''}
                </p>
              )}
            </div>
            <div>
              <label className="text-muted">接口地址（Base URL，可选）</label>
              <input
                className="input mt-1"
                value={llmBaseUrl}
                onChange={(e) => setLlmBaseUrl(e.target.value)}
                placeholder="留空使用提供商默认地址"
                spellCheck={false}
              />
              <p className="mt-1 text-xs text-faint">
                网关/代理（如 One API）填写对应 /v1 地址；留空 = 提供商官方地址。
              </p>
            </div>
            <div>
              <label className="text-muted">API Key</label>
              <div className="mt-1 flex items-start gap-2">
                <div className="flex-1">
                  <PasswordField
                    value={apiKey}
                    onChange={(v) => {
                      setApiKey(v)
                      if (v) setClearKey(false)
                    }}
                    placeholder={
                      llm?.api_key_set
                        ? '已设置，留空不修改'
                        : keyConfigured
                          ? '系统已配置默认密钥，输入可覆盖'
                          : '输入 API Key'
                    }
                    disabled={clearKey}
                  />
                </div>
                {llm?.api_key_set && (
                  <button
                    type="button"
                    className="btn btn-ghost shrink-0 px-3 py-2 text-xs"
                    onClick={() => {
                      setApiKey('')
                      setClearKey(true)
                    }}
                  >
                    清除
                  </button>
                )}
              </div>
              <p className="mt-1 text-xs text-faint">密钥加密存储，不会明文回显。</p>
            </div>
            <div>
              <label className="text-muted">模型</label>
              <div className="mt-1">
                <ModelPicker
                  providerId={provider}
                  model={model}
                  models={modelOptions}
                  onChange={setModel}
                />
              </div>
              {provider && (llmFetching || llmFetchNote) && (
                <p className="mt-1 text-xs text-faint">
                  {llmFetching
                    ? '正在在线拉取模型列表…'
                    : llmFetchNote ?? '模型列表已在线拉取'}
                </p>
              )}
            </div>
            <div>
              <label className="flex items-center justify-between text-muted">
                <span>Temperature（生成随机性）</span>
                <span className="tabular-nums text-ink">{temperature.toFixed(1)}</span>
              </label>
              <input
                className="mt-2 w-full accent-primary"
                type="range"
                min={0}
                max={2}
                step={0.1}
                value={temperature}
                onChange={(e) => setTemperature(Number(e.target.value))}
              />
            </div>
            <SaveRow
              state={llmSave}
              onSave={() => void saveLlm()}
              extra={
                hasOverride ? (
                  <button
                    type="button"
                    className="btn btn-ghost px-3 py-2 text-xs"
                    onClick={() => void restoreLlmDefault()}
                    disabled={llmSave.saving}
                  >
                    恢复系统默认
                  </button>
                ) : undefined
              }
            />
          </div>
        ) : (
          <p className="text-sm text-faint">加载中…</p>
        )}
      </section>

      {/* 知识库 */}
      <section className="card p-6">
        <h2 className="mb-4 text-base font-semibold">知识库</h2>
        {!authed ? (
          <p className="text-sm text-muted">
            登录后可配置检索参数。
            <button type="button" className="ml-2 text-primary" onClick={openLoginModal}>
              点击登录
            </button>
          </p>
        ) : settings ? (
          <div className="space-y-4 text-sm">
            {/* 嵌入模型（独立于对话 LLM，provider 为 NULL 时继承 .env） */}
            <div className="space-y-4 border-b border-border pb-4">
              <h3 className="text-sm font-medium text-ink">嵌入模型</h3>
              {embEff?.warning && (
                <p className="rounded-lg bg-danger/10 px-3 py-2 text-xs leading-relaxed text-danger">
                  {embEff.warning}
                </p>
              )}
              <div>
                <label className="text-muted">嵌入模型提供商</label>
                <select
                  className="input mt-1"
                  value={embedProvider}
                  onChange={(e) => onEmbedProviderChange(e.target.value)}
                >
                  {!embedProvider && <option value="">请选择提供商</option>}
                  {settings.embed_providers.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name}
                    </option>
                  ))}
                </select>
                {!embedHasOverride && embEff && (
                  <p className="mt-1 text-xs text-faint">
                    未自定义，当前使用系统默认：
                    {settings.embed_providers.find((p) => p.id === embEff.provider)?.name ??
                      embEff.base_url}{' '}
                    / {embEff.model ?? ''}
                  </p>
                )}
              </div>
              <div>
                <label className="text-muted">接口地址（Base URL，可选）</label>
                <input
                  className="input mt-1"
                  value={embedBaseUrl}
                  onChange={(e) => setEmbedBaseUrl(e.target.value)}
                  placeholder="留空使用提供商默认地址"
                  spellCheck={false}
                />
                <p className="mt-1 text-xs text-faint">
                  网关/代理（如 One API）填写对应 /v1 地址；留空 = 提供商官方地址。
                </p>
              </div>
              <div>
                <label className="text-muted">嵌入模型 API Key</label>
                <div className="mt-1 flex items-start gap-2">
                  <div className="flex-1">
                    <PasswordField
                      value={embedApiKey}
                      onChange={(v) => {
                        setEmbedApiKey(v)
                        if (v) setEmbedClearKey(false)
                      }}
                      placeholder={
                        emb?.api_key_set
                          ? '已设置，留空不修改'
                          : embedKeyConfigured
                            ? '系统已配置默认密钥，输入可覆盖'
                            : '输入 API Key（Ollama 本地无需）'
                      }
                      disabled={embedClearKey}
                    />
                  </div>
                  {emb?.api_key_set && (
                    <button
                      type="button"
                      className="btn btn-ghost shrink-0 px-3 py-2 text-xs"
                      onClick={() => {
                        setEmbedApiKey('')
                        setEmbedClearKey(true)
                      }}
                    >
                      清除
                    </button>
                  )}
                </div>
                <p className="mt-1 text-xs text-faint">
                  密钥加密存储，不会明文回显；更换嵌入模型后建议重新上传文档。
                </p>
              </div>
              <div>
                <label className="text-muted">嵌入模型</label>
                <div className="mt-1">
                  <ModelPicker
                    providerId={embedProvider}
                    model={embedModel}
                    models={embedModelOptions}
                    onChange={setEmbedModel}
                  />
                </div>
                {embedProvider && (embedFetching || embedFetchNote) && (
                  <p className="mt-1 text-xs text-faint">
                    {embedFetching
                      ? '正在在线拉取模型列表…'
                      : embedFetchNote ?? '模型列表已在线拉取'}
                  </p>
                )}
              </div>
            </div>
            <div className="flex items-center gap-3">
              <label className="w-28 shrink-0 text-muted">默认检索数 k</label>
              <input
                className="input w-28"
                type="number"
                min={1}
                max={20}
                value={topK}
                onChange={(e) => setTopK(Math.min(20, Math.max(1, Number(e.target.value) || 1)))}
              />
              <span className="text-xs text-faint">问答时召回的知识块数量（1–20）</span>
            </div>
            <div className="flex items-center gap-3">
              <label className="w-28 shrink-0 text-muted">块大小 chunk_size</label>
              <input
                className="input w-28"
                type="number"
                min={200}
                max={8000}
                step={100}
                value={chunkSize}
                onChange={(e) =>
                  setChunkSize(Math.min(8000, Math.max(200, Number(e.target.value) || 200)))
                }
              />
              <span className="text-xs text-faint">文档切分块大小（200–8000）</span>
            </div>
            <div>
              <label className="flex items-center justify-between text-muted">
                <span>相似度阈值</span>
                <span className="tabular-nums text-ink">{threshold.toFixed(2)}</span>
              </label>
              <input
                className="mt-2 w-full accent-primary"
                type="range"
                min={0}
                max={1}
                step={0.01}
                value={threshold}
                onChange={(e) => setThreshold(Number(e.target.value))}
              />
              <p className="mt-1 text-xs text-faint">低于该相关度的检索块会被过滤（0 = 不过滤）</p>
            </div>
            <SaveRow
              state={kbSave}
              onSave={() => void saveKb()}
              extra={
                embedHasOverride ||
                settings.kb.top_k != null ||
                settings.kb.chunk_size != null ||
                settings.kb.similarity_threshold != null ? (
                  <button
                    type="button"
                    className="btn btn-ghost px-3 py-2 text-xs"
                    onClick={() => void restoreKbDefault()}
                    disabled={kbSave.saving}
                  >
                    恢复系统默认
                  </button>
                ) : undefined
              }
            />
          </div>
        ) : (
          <p className="text-sm text-faint">加载中…</p>
        )}
      </section>

      {/* 个人信息 */}
      <section className="card p-6">
        <h2 className="mb-4 text-base font-semibold">个人信息</h2>
        {!authed ? (
          <p className="text-sm text-muted">
            未登录。
            <button type="button" className="ml-2 text-primary" onClick={openLoginModal}>
              点击登录
            </button>
          </p>
        ) : (
          <div className="space-y-4 text-sm">
            <div className="flex items-center gap-4">
              <Avatar name={user?.username ?? ''} src={displayAvatar} size={56} />
              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <input
                    ref={avatarInputRef}
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={onAvatarPick}
                  />
                  <button
                    type="button"
                    className="btn btn-ghost px-3 py-1.5 text-xs"
                    onClick={() => avatarInputRef.current?.click()}
                  >
                    <Camera size={14} /> 选择图片
                  </button>
                  {avatarFile && (
                    <button
                      type="button"
                      className="btn btn-primary px-3 py-1.5 text-xs"
                      onClick={() => void saveAvatar()}
                      disabled={profileSave.saving}
                    >
                      上传
                    </button>
                  )}
                  {user?.avatar && !avatarPreview && (
                    <button
                      type="button"
                      className="btn btn-ghost px-3 py-1.5 text-xs text-danger hover:bg-danger/10"
                      onClick={() => void removeAvatar()}
                      disabled={profileSave.saving}
                    >
                      <Trash2 size={14} /> 移除
                    </button>
                  )}
                </div>
                <p className="text-xs text-faint">支持 JPG/PNG 等，最大 5MB，自动压缩为方形头像。</p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <label className="w-28 shrink-0 pt-2 text-muted">用户名</label>
              <div className="flex-1">
                <input
                  className="input"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="3–20 位字母/数字/下划线"
                />
              </div>
            </div>

            <div className="flex items-center gap-3">
              <label className="w-28 shrink-0 text-muted">邮箱</label>
              <span className="text-ink">{user?.email}</span>
              <span className="text-xs text-faint">（只读）</span>
            </div>

            <div className="flex items-center gap-3">
              <label className="w-28 shrink-0 text-muted">创建时间</label>
              <span className="text-ink">{user ? formatDateTime(user.created_at) : ''}</span>
            </div>

            <div className="flex items-center gap-3">
              <label className="w-28 shrink-0 text-muted">密码</label>
              <button
                type="button"
                className="btn btn-ghost px-3 py-2 text-xs"
                onClick={() => setShowPwModal(true)}
              >
                <KeyRound size={14} /> 修改密码
              </button>
            </div>

            {profileSave.msg && <p className="text-sm text-ok">{profileSave.msg}</p>}
            {profileSave.err && <p className="break-all text-sm text-danger">{profileSave.err}</p>}
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => void saveUsername()}
              disabled={profileSave.saving}
            >
              保存用户名
            </button>
          </div>
        )}
      </section>

      {/* 外观偏好 */}
      <section className="card p-6">
        <h2 className="mb-4 text-base font-semibold">外观偏好</h2>
        <div className="space-y-4 text-sm">
          <div>
            <p className="mb-2 text-muted">主题模式</p>
            <div className="flex gap-1 rounded-lg bg-bg p-1">
              {(
                [
                  ['light', '浅色'],
                  ['dark', '深色'],
                  ['system', '跟随系统'],
                ] as const
              ).map(([value, label]) => (
                <button
                  key={value}
                  type="button"
                  className={`flex-1 rounded-md px-3 py-1.5 text-sm transition-colors ${
                    prefs.theme === value
                      ? 'bg-panel font-medium text-ink shadow-sm'
                      : 'text-muted hover:text-ink'
                  }`}
                  onClick={() => prefs.update({ theme: value as ThemeMode })}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
          <div className="flex items-center gap-3">
            <ToggleSwitch
              checked={prefs.sidebarCollapsed}
              onChange={(v) => prefs.update({ sidebarCollapsed: v })}
              label="侧边栏收起"
            />
            <div>
              <p className="text-ink">侧边栏收起</p>
              <p className="text-xs text-faint">收起后仅显示图标，为内容区留出更多空间</p>
            </div>
          </div>
          <p className="text-xs text-faint">
            外观偏好保存在本机，登录后会同步到账号（跨设备生效）。
          </p>
        </div>
      </section>

      {/* 关于 */}
      <section className="card p-6">
        <h2 className="mb-4 text-base font-semibold">关于</h2>
        <p className="mb-2 flex items-center gap-2 text-sm font-medium">
          <BookOpen size={16} className="text-primary" /> 智能笔记
        </p>
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted">
          {STACK.map((s) => (
            <li key={s}>{s}</li>
          ))}
        </ul>
        <p className="mt-3 text-xs text-muted">版本：{health?.version ?? 'dev'}</p>
      </section>

      {showPwModal && <ChangePasswordModal onClose={() => setShowPwModal(false)} />}
    </div>
  )
}

function SaveRow({
  state,
  onSave,
  extra,
}: {
  state: SaveState
  onSave: () => void
  extra?: React.ReactNode
}) {
  return (
    <div className="flex items-center gap-3 border-t border-border pt-3">
      <button type="button" className="btn btn-primary" onClick={onSave} disabled={state.saving}>
        {state.saving ? '保存中…' : '保存'}
      </button>
      {state.msg && <span className="text-sm text-ok">{state.msg}</span>}
      {state.err && <span className="break-all text-sm text-danger">{state.err}</span>}
      {extra && <span className="ml-auto">{extra}</span>}
    </div>
  )
}
