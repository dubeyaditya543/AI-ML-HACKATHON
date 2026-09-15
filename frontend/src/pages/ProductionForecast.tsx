import Card from '../components/ui/Card'
import StatBlock from '../components/ui/StatBlock'
import ForecastChart from '../components/charts/ForecastChart'
import { FORECAST_DATA } from '../data/mockData'

export default function ProductionForecast() {
  const latestActual = [...FORECAST_DATA].reverse().find((p) => p.actual !== null)
  const last30 = FORECAST_DATA.slice(-14)
  const avgForecast = Math.round(last30.reduce((sum, p) => sum + p.forecast, 0) / last30.length)
  const target = FORECAST_DATA[0]?.target ?? 0

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold">Production Forecast</h1>
        <p className="text-sm text-text-muted mt-1">
          Actual vs forecast vs target — 7-day, 30-day, and monthly horizons
        </p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <Card>
          <StatBlock label="Latest Actual" value={latestActual?.actual?.toLocaleString() ?? '—'} unit="t/day" />
        </Card>
        <Card>
          <StatBlock label="Avg. Forecast (next 14d)" value={avgForecast.toLocaleString()} unit="t/day" tone="ore" />
        </Card>
        <Card>
          <StatBlock label="Daily Target" value={target.toLocaleString()} unit="t/day" tone="positive" />
        </Card>
      </div>

      <Card title="Actual vs Forecast vs Target">
        <ForecastChart data={FORECAST_DATA} />
      </Card>

      <Card title="Data Category" className="border-ore/30">
        <p className="text-xs text-text-muted leading-relaxed">
          Time series shown is a <span className="text-ore">Demonstration Synthetic Dataset</span> generated to
          mimic realistic daily production variance. Model selection (ARIMA / Prophet / RF / XGBoost / LSTM)
          happens against historical MOIL production data in the backend — see Module 6.
        </p>
      </Card>
    </div>
  )
}