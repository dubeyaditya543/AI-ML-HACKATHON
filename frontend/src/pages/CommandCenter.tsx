import { TrendingUp, TrendingDown, Target, Layers, AlertTriangle } from 'lucide-react'
import Card from '../components/ui/Card'
import StatBlock from '../components/ui/StatBlock'
import Badge from '../components/ui/Badge'
import { COMMAND_CENTER_SUMMARY, MINE_BLOCKS, RISK_RECORDS } from '../data/mockData'

export default function CommandCenter() {
  const s = COMMAND_CENTER_SUMMARY
  const gapPct = Math.round(((s.targetProduction - s.predictedProduction) / s.targetProduction) * 100)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold">Executive Command Center</h1>
        <p className="text-sm text-text-muted mt-1">
          Fleet-wide production outlook and reserve status across active mine blocks
        </p>
      </div>

      {/* Top stat row */}
      <div className="grid grid-cols-5 gap-4">
        <Card>
          <div className="flex items-start justify-between">
            <StatBlock label="Predicted Production" value={s.predictedProduction.toLocaleString()} unit="t" />
            {gapPct > 0 ? (
              <TrendingDown size={16} className="text-risk mt-1" />
            ) : (
              <TrendingUp size={16} className="text-positive mt-1" />
            )}
          </div>
        </Card>
        <Card>
          <StatBlock label="Target Production" value={s.targetProduction.toLocaleString()} unit="t" />
        </Card>
        <Card>
          <div className="flex items-start justify-between">
            <StatBlock label="Shortfall Risk" value={s.shortfallRiskPct} unit="%" tone="risk" />
            <AlertTriangle size={16} className="text-risk mt-1" />
          </div>
        </Card>
        <Card>
          <StatBlock label="Recoverable Production" value={s.recoverableProduction.toLocaleString()} unit="t" tone="positive" />
        </Card>
        <Card>
          <div className="flex items-start justify-between">
            <StatBlock label="High Prospectivity Areas" value={s.highProspectivityAreaCount} tone="ore" />
            <Layers size={16} className="text-ore mt-1" />
          </div>
        </Card>
      </div>

      {/* Lower row: mine block status + highest-risk mines */}
      <div className="grid grid-cols-2 gap-4">
        <Card title="Mine Block Status">
          <div className="space-y-2">
            {MINE_BLOCKS.map((m) => (
              <div key={m.id} className="flex items-center justify-between py-1.5 border-b border-border last:border-0">
                <span className="text-sm">{m.name}</span>
                <span
                  className={
                    m.status === 'Active'
                      ? 'text-xs font-mono text-positive'
                      : m.status === 'Maintenance'
                      ? 'text-xs font-mono text-ore'
                      : 'text-xs font-mono text-text-muted'
                  }
                >
                  {m.status.toUpperCase()}
                </span>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Highest Shortfall Risk" action={<Target size={14} className="text-text-muted" />}>
          <div className="space-y-2">
            {[...RISK_RECORDS]
              .sort((a, b) => b.riskScore - a.riskScore)
              .slice(0, 4)
              .map((r) => (
                <div key={r.mineId} className="flex items-center justify-between py-1.5 border-b border-border last:border-0">
                  <div>
                    <p className="text-sm">{r.mineName}</p>
                    <p className="text-xs text-text-muted font-mono">
                      Shortfall: {r.shortfallAmount.toLocaleString()} t
                    </p>
                  </div>
                  <Badge label={r.riskTier} />
                </div>
              ))}
          </div>
        </Card>
      </div>
    </div>
  )
}