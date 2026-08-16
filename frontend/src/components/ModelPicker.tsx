import { useState } from 'react'

const CUSTOM = '__custom__'

interface ModelPickerProps {
  /** 当前所选 provider id；变化时 remount 以重置自定义编辑态 */
  providerId: string
  model: string
  /** 该 provider 的建议模型列表（顺序即下拉展示顺序） */
  models: string[]
  onChange: (model: string) => void
}

/**
 * 模型选择器：建议列表下拉 + 「自定义模型…」文本输入。
 *
 * Ollama 本地 / 厂商新模型的 ID 不在注册表里，需要允许手输任意模型 ID；
 * provider 切换时以 key={providerId} 强制 remount，清掉上一个 provider 的编辑态。
 */
export default function ModelPicker({
  providerId,
  model,
  models,
  onChange,
}: ModelPickerProps) {
  // 初始值不在建议列表（加载了已存的本地/自定义模型）-> 直接进入编辑态
  const [custom, setCustom] = useState(() => !models.includes(model))

  return (
    <div key={providerId} className="space-y-2">
      <select
        className="input"
        value={custom ? CUSTOM : model}
        onChange={(e) => {
          if (e.target.value === CUSTOM) {
            setCustom(true)
          } else {
            setCustom(false)
            onChange(e.target.value)
          }
        }}
      >
        {models.map((m) => (
          <option key={m} value={m}>
            {m}
          </option>
        ))}
        <option value={CUSTOM}>自定义模型…</option>
      </select>
      {custom && (
        <input
          className="input"
          value={model}
          onChange={(e) => onChange(e.target.value)}
          placeholder="输入模型 ID（如 nomic-embed-text）"
        />
      )}
    </div>
  )
}
