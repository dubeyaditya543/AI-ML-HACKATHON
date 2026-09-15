import { useMemo, useState } from "react";
import Card from "../components/ui/Card";
import StatBlock from "../components/ui/StatBlock";
import CategoryIcon from "../components/ui/CategoryIcon";
import { RECOMMENDATIONS } from "../data/mockData";

export default function RecommendationCenter() {
  const [applied, setApplied] = useState<Set<string>>(new Set());
  const [loaderShift, setLoaderShift] = useState(0); // 0-3 loaders
  const [blastAdvanceDays, setBlastAdvanceDays] = useState(0); // 0-3 days

  const totalRecovery = useMemo(
    () =>
      RECOMMENDATIONS.filter((r) => applied.has(r.id)).reduce(
        (sum, r) => sum + r.expectedRecoveryTonnes,
        0,
      ),
    [applied],
  );

  const simulatedRecovery = loaderShift * 950 + blastAdvanceDays * 800;

  function toggle(id: string) {
    setApplied((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold">AI Recommendation Center</h1>
        <p className="text-sm text-text-muted mt-1">
          Optimization-engine outputs and what-if simulation controls
        </p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <Card>
          <StatBlock
            label="Recommendations Applied"
            value={applied.size}
            unit={`/ ${RECOMMENDATIONS.length}`}
          />
        </Card>
        <Card>
          <StatBlock
            label="Recovery from Applied"
            value={totalRecovery.toLocaleString()}
            unit="t"
            tone="positive"
          />
        </Card>
        <Card>
          <StatBlock
            label="What-If Simulated Recovery"
            value={simulatedRecovery.toLocaleString()}
            unit="t"
            tone="ore"
          />
        </Card>
      </div>

      <div className="grid grid-cols-5 gap-4">
        <div className="col-span-3">
          <Card title="Optimization Engine Output" className="p-0">
            <div className="divide-y divide-border">
              {RECOMMENDATIONS.map((r) => {
                const isApplied = applied.has(r.id);
                return (
                  <div key={r.id} className="p-4 flex items-start gap-3">
                    <div className="mt-0.5 text-ore">
                      <CategoryIcon category={r.category} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium">{r.action}</p>
                        <span className="text-xs font-mono text-positive">
                          +{r.expectedRecoveryTonnes.toLocaleString()} t
                        </span>
                      </div>
                      <p className="text-xs text-text-muted mt-1 leading-relaxed">
                        {r.detail}
                      </p>
                    </div>
                    <button
                      onClick={() => toggle(r.id)}
                      className={`shrink-0 text-xs font-mono px-3 py-1.5 rounded-sm border transition-colors ${
                        isApplied
                          ? "bg-positive/15 text-positive border-positive/30"
                          : "text-text-muted border-border hover:text-text-primary hover:border-text-muted"
                      }`}
                    >
                      {isApplied ? "APPLIED" : "APPLY"}
                    </button>
                  </div>
                );
              })}
            </div>
          </Card>
        </div>

        <div className="col-span-2">
          <Card title="What-If Simulator">
            <div className="space-y-6">
              <div>
                <div className="flex items-center justify-between text-xs font-mono mb-2">
                  <span className="text-text-muted">Loaders reallocated</span>
                  <span className="text-ore">{loaderShift}</span>
                </div>
                <input
                  type="range"
                  min={0}
                  max={3}
                  step={1}
                  value={loaderShift}
                  onChange={(e) => setLoaderShift(Number(e.target.value))}
                  className="w-full accent-[#C97B2E]"
                />
              </div>

              <div>
                <div className="flex items-center justify-between text-xs font-mono mb-2">
                  <span className="text-text-muted">Blast advance (days)</span>
                  <span className="text-ore">{blastAdvanceDays}</span>
                </div>
                <input
                  type="range"
                  min={0}
                  max={3}
                  step={1}
                  value={blastAdvanceDays}
                  onChange={(e) => setBlastAdvanceDays(Number(e.target.value))}
                  className="w-full accent-[#C97B2E]"
                />
              </div>

              <div className="pt-4 border-t border-border">
                <p className="text-xs text-text-muted leading-relaxed">
                  Simulator uses simplified per-unit recovery estimates for
                  demonstration. Production version solves the full constrained
                  optimization (OR-Tools) across equipment capacity, mine
                  capacity, working hours, and safety buffers — Module 8.
                </p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
