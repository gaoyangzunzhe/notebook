import { useMemo } from 'react'

/** 由用户名确定性推导底色，同一用户始终同色 */
function hashColor(name: string): string {
  let h = 0
  for (const ch of name) h = (h * 31 + (ch.codePointAt(0) ?? 0)) % 360
  return `hsl(${h} 45% 45%)`
}

/** 头像：有 src（data URL）时显示图片，否则显示首字母底色块。 */
export default function Avatar({
  name,
  src,
  size = 32,
}: {
  name: string
  src?: string | null
  size?: number
}) {
  const initial = useMemo(() => (name.trim() ? name.trim()[0].toUpperCase() : '?'), [name])

  if (src) {
    return (
      <img
        src={src}
        alt={name}
        title={name}
        className="shrink-0 select-none rounded-full object-cover"
        style={{ width: size, height: size }}
      />
    )
  }

  return (
    <div
      className="flex shrink-0 select-none items-center justify-center rounded-full font-semibold text-white"
      style={{ width: size, height: size, background: hashColor(name), fontSize: size * 0.45 }}
      title={name}
    >
      {initial}
    </div>
  )
}
