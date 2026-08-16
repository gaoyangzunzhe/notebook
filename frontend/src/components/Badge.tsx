type Tone = 'ok' | 'danger' | 'muted' | 'info'

const tones: Record<Tone, string> = {
  ok: 'bg-ok/10 text-ok',
  danger: 'bg-danger/10 text-danger',
  muted: 'bg-muted/10 text-muted',
  info: 'bg-primary-weak text-primary',
}

export default function Badge({
  tone = 'muted',
  children,
}: {
  tone?: Tone
  children: React.ReactNode
}) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${tones[tone]}`}
    >
      {children}
    </span>
  )
}
