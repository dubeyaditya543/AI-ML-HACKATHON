import clsx from 'clsx'

const TIER_CLASSES: Record<string, string> = {
  Low: 'bg-positive/15 text-positive border-positive/30',
  Moderate: 'bg-ore/15 text-ore border-ore/30',
  High: 'bg-risk/15 text-risk border-risk/30',
  Critical: 'bg-risk/25 text-risk border-risk/50',
}

export default function Badge({ label }: { label: string }) {
  return (
    <span
      className={clsx(
        'inline-flex items-center px-2 py-0.5 rounded-sm text-xs font-mono border',
        TIER_CLASSES[label] ?? 'bg-bg-panel-hover text-text-muted border-border'
      )}
    >
      {label}
    </span>
  )
}