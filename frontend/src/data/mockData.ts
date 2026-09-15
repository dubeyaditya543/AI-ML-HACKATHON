import type {
  ProspectivityCell,
  DrillHole,
  MineBlock,
  ForecastPoint,
  RiskRecord,
  Recommendation,
  CommandCenterSummary,
} from '../types'

// Demonstration Synthetic Dataset — not MOIL confidential data.
// Coordinates loosely follow MOIL's real mining belts (Balaghat, MP &
// Nagpur cluster, Maharashtra) for geographic plausibility only.

export const MINE_BLOCKS: MineBlock[] = [
  { id: 'mn-01', name: 'Balaghat Mine', lat: 21.8064, lng: 80.1907, status: 'Active' },
  { id: 'mn-02', name: 'Ukwa Mine', lat: 21.7532, lng: 80.2216, status: 'Active' },
  { id: 'mn-03', name: 'Dongri Buzurg Mine', lat: 21.1685, lng: 79.2013, status: 'Active' },
  { id: 'mn-04', name: 'Gumgaon Mine', lat: 21.0521, lng: 79.0247, status: 'Maintenance' },
  { id: 'mn-05', name: 'Kandri Mine', lat: 21.2489, lng: 79.1532, status: 'Active' },
  { id: 'mn-06', name: 'Munsar Mine', lat: 21.2871, lng: 79.1105, status: 'Idle' },
]

export const PROSPECTIVITY_CELLS: ProspectivityCell[] = Array.from({ length: 36 }).map((_, i) => {
  const base = MINE_BLOCKS[i % MINE_BLOCKS.length]
  const jitter = () => (Math.random() - 0.5) * 0.08
  const score = Math.round(35 + Math.random() * 60)
  return {
    id: `cell-${i + 1}`,
    lat: base.lat + jitter(),
    lng: base.lng + jitter(),
    prospectivityScore: score,
    confidence: Math.round(55 + Math.random() * 40),
    predictedGrade: +(18 + Math.random() * 22).toFixed(1),
    recommendedAction: score > 75 ? 'Exploration Drilling' : score > 50 ? 'Monitor' : 'Low Priority',
  }
})

export const DRILL_HOLES: DrillHole[] = Array.from({ length: 18 }).map((_, i) => {
  const base = MINE_BLOCKS[i % MINE_BLOCKS.length]
  const jitter = () => (Math.random() - 0.5) * 0.06
  return {
    id: `dh-${String(i + 1).padStart(3, '0')}`,
    lat: base.lat + jitter(),
    lng: base.lng + jitter(),
    depth: Math.round(40 + Math.random() * 160),
    mnGrade: +(15 + Math.random() * 25).toFixed(1),
    rockType: ['Gondite', 'Kodurite', 'Ferruginous Shale', 'Quartzite'][i % 4],
    sampleDate: `2026-0${(i % 6) + 3}-${String(((i * 3) % 27) + 1).padStart(2, '0')}`,
  }
})

function buildForecast(): ForecastPoint[] {
  const points: ForecastPoint[] = []
  const target = 1450
  let actualTrend = 1300
  for (let day = 0; day < 44; day++) {
    const date = new Date(2026, 7, 1 + day).toISOString().slice(0, 10)
    const isFuture = day >= 30
    actualTrend += (Math.random() - 0.45) * 60
    const forecastVal = Math.round(actualTrend + (Math.random() - 0.5) * 40)
    points.push({
      date,
      actual: isFuture ? null : Math.round(actualTrend),
      forecast: forecastVal,
      target,
    })
  }
  return points
}
export const FORECAST_DATA: ForecastPoint[] = buildForecast()

export const RISK_RECORDS: RiskRecord[] = [
  {
    mineId: 'mn-01',
    mineName: 'Balaghat Mine',
    riskScore: 72,
    riskTier: 'High',
    predictedProduction: 1180,
    targetProduction: 1450,
    shortfallAmount: 270,
    causes: [
      { cause: 'Equipment Downtime', contributionPct: 31 },
      { cause: 'Rainfall', contributionPct: 22 },
      { cause: 'Blasting Delay', contributionPct: 18 },
      { cause: 'Ore Availability', contributionPct: 15 },
      { cause: 'Other', contributionPct: 14 },
    ],
  },
  {
    mineId: 'mn-02',
    mineName: 'Ukwa Mine',
    riskScore: 38,
    riskTier: 'Moderate',
    predictedProduction: 890,
    targetProduction: 950,
    shortfallAmount: 60,
    causes: [
      { cause: 'Rainfall', contributionPct: 34 },
      { cause: 'Truck Availability', contributionPct: 26 },
      { cause: 'Blasting Delay', contributionPct: 20 },
      { cause: 'Other', contributionPct: 20 },
    ],
  },
  {
    mineId: 'mn-04',
    mineName: 'Gumgaon Mine',
    riskScore: 88,
    riskTier: 'Critical',
    predictedProduction: 410,
    targetProduction: 800,
    shortfallAmount: 390,
    causes: [
      { cause: 'Equipment Downtime', contributionPct: 46 },
      { cause: 'Maintenance Backlog', contributionPct: 28 },
      { cause: 'Ore Availability', contributionPct: 14 },
      { cause: 'Other', contributionPct: 12 },
    ],
  },
  {
    mineId: 'mn-05',
    mineName: 'Kandri Mine',
    riskScore: 19,
    riskTier: 'Low',
    predictedProduction: 720,
    targetProduction: 700,
    shortfallAmount: 0,
    causes: [
      { cause: 'Weather Variability', contributionPct: 40 },
      { cause: 'Other', contributionPct: 60 },
    ],
  },
]

export const RECOMMENDATIONS: Recommendation[] = [
  {
    id: 'rec-1',
    action: 'Move Loader L04 → Ukwa Mine',
    detail: 'Balaghat loader utilization exceeds capacity; Ukwa has 18% idle loader time this week.',
    expectedRecoveryTonnes: 3800,
    category: 'Equipment',
  },
  {
    id: 'rec-2',
    action: 'Advance Blast B17',
    detail: 'Rescheduling 2 days earlier avoids forecast rainfall window at Gumgaon.',
    expectedRecoveryTonnes: 2400,
    category: 'Blasting',
  },
  {
    id: 'rec-3',
    action: 'Shift 3 Trucks to Balaghat',
    detail: 'Truck availability at Kandri exceeds demand; reallocation reduces haulage bottleneck.',
    expectedRecoveryTonnes: 2100,
    category: 'Scheduling',
  },
  {
    id: 'rec-4',
    action: 'Prioritize Block X17',
    detail: 'Highest prospectivity-confidence block currently below planned extraction rate.',
    expectedRecoveryTonnes: 1500,
    category: 'Prioritization',
  },
]

export const COMMAND_CENTER_SUMMARY: CommandCenterSummary = {
  predictedProduction: 4210,
  targetProduction: 4900,
  shortfallRiskPct: 34,
  recoverableProduction: 3200,
  highProspectivityAreaCount: 9,
}