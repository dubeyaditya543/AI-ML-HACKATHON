import { Routes, Route } from 'react-router-dom'
import AppShell from './components/layout/AppShell'
import CommandCenter from './pages/CommandCenter'
import ProspectivityMap from './pages/ProspectivityMap'
import ProductionForecast from './pages/ProductionForecast'
import RiskAnalysis from './pages/RiskAnalysis'
import RecommendationCenter from './pages/RecommendationCenter'


export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<CommandCenter />} />
        <Route path="/prospectivity" element={<ProspectivityMap />} />
        <Route path="/forecast" element={<ProductionForecast />} />
        <Route path="/risk" element={<RiskAnalysis />} />
        <Route path="/recommendations" element={<RecommendationCenter />} />
      </Routes>
    </AppShell>
  )
}