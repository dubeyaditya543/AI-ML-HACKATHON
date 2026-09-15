import clsx from 'clsx'

export default function StatBlock({
  label,
  value,
  unit,
  tone = 'default',
}: {
  label: string
  value: string | number
  unit?: string
  tone?: 'default' | 'ore' | 'risk' | 'positive'
}) {
  const toneClass = {
    default: 'text-text-primary',
    ore: 'text-ore',
    risk: 'text-risk',
    positive: 'text-positive',
  }[tone]

  return (
    <div className="space-y-1">
      <p className="text-xs text-text-muted uppercase tracking-wide">{label}</p>
      <p className={clsx('font-mono text-2xl font-medium', toneClass)}>
        {value}
        {unit && <span className="text-sm text-text-muted ml-1">{unit}</span>}
      </p>
    </div>
  )
}