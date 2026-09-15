import { useState } from 'react'
import { HelpCircle } from 'lucide-react'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import CauseBreakdownChart from '../components/charts/CauseBreakdownChart'
import { RISK_RECORDS } from '../data/mockData'

export default function RiskAnalysis() {
  const [selectedMineId, setSelectedMineId] = useState(RISK_RECORDS[0]?.mineId ?? '')
  const selected = RISK_RECORDS.find((r) => r.mineId === selectedMineId) ?? RISK_RECORDS[0]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold">Risk Analysis</h1>
        <p className="text-sm text-text-muted mt-1">
          Mine-wise shortfall risk with SHAP-based cause attribution
        </p>
      </div>

      <div className="grid grid-cols-5 gap-4">
        <div className="col-span-2">
          <Card title="Mine-wise Risk" className="p-0">
            <div className="divide-y divide-border">
              {RISK_RECORDS.map((r) => (
                <button
                  key={r.mineId}
                  onClick={() => setSelectedMineId(r.mineId)}
                  className={`w-full text-left px-4 py-3 transition-colors ${
                    r.mineId === selectedMineId ? 'bg-bg-panel-hover' : 'hover:bg-bg-panel-hover'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm">{r.mineName}</span>
                    <Badge label={r.riskTier} />
                  </div>
                  <div className="flex items-center justify-between text-xs font-mono text-text-muted">
                    <span>
                      {r.predictedProduction.toLocaleString()} / {r.targetProduction.toLocaleString()} t
                    </span>
                    <span>Risk {r.riskScore}%</span>
                  </div>
                </button>
              ))}
            </div>
          </Card>
        </div>

        <div className="col-span-3 space-y-4">
          {selected && (
            <>
              <Card
                title={`${selected.mineName} — Why did AI predict this?`}
                action={<HelpCircle size={14} className="text-text-muted" />}
              >
                <div className="grid grid-cols-3 gap-4 mb-4 text-xs font-mono">
                  <div>
                    <p className="text-text-muted">Predicted</p>
                    <p className="text-text-primary text-sm mt-0.5">{selected.predictedProduction.toLocaleString()} t</p>
                  </div>
                  <div>
                    <p className="text-text-muted">Target</p>
                    <p className="text-text-primary text-sm mt-0.5">{selected.targetProduction.toLocaleString()} t</p>
                  </div>
                  <div>
                    <p className="text-text-muted">Shortfall</p>
                    <p className="text-risk text-sm mt-0.5">{selected.shortfallAmount.toLocaleString()} t</p>
                  </div>
                </div>
                <CauseBreakdownChart causes={selected.causes} />
              </Card>

              <Card title="Data Category" className="border-ore/30">
                <p className="text-xs text-text-muted leading-relaxed">
                  Risk scores and cause contributions are a{' '}
                  <span className="text-ore">Demonstration Synthetic Dataset</span>. In production this
                  panel is populated by SHAP values from the Shortfall Risk model (Module 7/9), not
                  hand-authored percentages.
                </p>
              </Card>
            </>
          )}
        </div>
      </div>
    </div>
  )
}