// ---------- Prospectivity (Module 4) ----------
export interface ProspectivityCell {
  id: string
  lat: number
  lng: number
  prospectivityScore: number // 0-100
  confidence: number // 0-100
  predictedGrade: number // Mn %
  recommendedAction: 'Exploration Drilling' | 'Monitor' | 'Low Priority'
}

export interface DrillHole {
  id: string
  lat: number
  lng: number
  depth: number
  mnGrade: number
  rockType: string
  sampleDate: string
}

export interface MineBlock {
  id: string
  name: string
  lat: number
  lng: number
  status: 'Active' | 'Idle' | 'Maintenance'
}

// ---------- Production Forecast (Module 6) ----------
export interface ForecastPoint {
  date: string
  actual: number | null
  forecast: number
  target: number
}

// ---------- Shortfall Risk (Module 7) ----------
export type RiskTier = 'Low' | 'Moderate' | 'High' | 'Critical'

export interface CauseContribution {
  cause: string
  contributionPct: number
}

export interface RiskRecord {
  mineId: string
  mineName: string
  riskScore: number // 0-100
  riskTier: RiskTier
  predictedProduction: number
  targetProduction: number
  shortfallAmount: number
  causes: CauseContribution[]
}

// ---------- Recommendation Engine (Module 8) ----------
export interface Recommendation {
  id: string
  action: string
  detail: string
  expectedRecoveryTonnes: number
  category: 'Equipment' | 'Blasting' | 'Scheduling' | 'Prioritization'
}

// ---------- Command Center summary (Page 1) ----------
export interface CommandCenterSummary {
  predictedProduction: number
  targetProduction: number
  shortfallRiskPct: number
  recoverableProduction: number
  highProspectivityAreaCount: number
}