import { Truck, Zap, CalendarClock, ArrowUpRight } from 'lucide-react'
import type { Recommendation } from '../../types'

const ICONS: Record<Recommendation['category'], typeof Truck> = {
  Equipment: Truck,
  Blasting: Zap,
  Scheduling: CalendarClock,
  Prioritization: ArrowUpRight,
}

export default function CategoryIcon({ category, size = 16 }: { category: Recommendation['category']; size?: number }) {
  const Icon = ICONS[category]
  return <Icon size={size} strokeWidth={2} />
}