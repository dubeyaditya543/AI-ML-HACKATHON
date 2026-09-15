import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  MapPinned,
  TrendingUp,
  ShieldAlert,
  Wand2,
  Radio,
} from 'lucide-react'
import type { ReactNode } from 'react'
import clsx from 'clsx'

const NAV_ITEMS = [
  { to: '/', label: 'Command Center', icon: LayoutDashboard },
  { to: '/prospectivity', label: 'Prospectivity Map', icon: MapPinned },
  { to: '/forecast', label: 'Production Forecast', icon: TrendingUp },
  { to: '/risk', label: 'Risk Analysis', icon: ShieldAlert },
  { to: '/recommendations', label: 'Recommendations', icon: Wand2 },
]

export default function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-screen w-screen bg-bg-base text-text-primary font-sans overflow-hidden">
      {/* Sidebar */}
      <aside className="w-60 shrink-0 border-r border-border bg-bg-panel flex flex-col">
        <div className="h-16 flex items-center gap-2 px-5 border-b border-border">
          <div className="w-2 h-2 rounded-full bg-ore" />
          <span className="font-semibold tracking-tight text-[15px]">
            MineVision <span className="text-ore">AI</span>
          </span>
        </div>

        <nav className="flex-1 py-4 px-3 space-y-1">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                clsx(
                  'flex items-center gap-3 px-3 py-2.5 rounded-sm text-sm transition-colors',
                  isActive
                    ? 'bg-bg-panel-hover text-ore border-l-2 border-ore -ml-[2px] pl-[14px]'
                    : 'text-text-muted hover:text-text-primary hover:bg-bg-panel-hover'
                )
              }
            >
              <Icon size={16} strokeWidth={2} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-border">
          <p className="text-[11px] text-text-muted font-mono leading-relaxed">
            MOIL LIMITED
            <br />
            Mn Reserve Intelligence
          </p>
        </div>
      </aside>

      {/* Main column */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top status strip */}
        <header className="h-16 shrink-0 border-b border-border bg-bg-panel flex items-center justify-between px-6">
          <div className="flex items-center gap-2 text-xs font-mono text-text-muted">
            <Radio size={14} className="text-positive" strokeWidth={2} />
            <span className="text-positive">LIVE</span>
            <span className="text-border">|</span>
            <span>Synthetic Demonstration Data</span>
          </div>
          <div className="text-xs font-mono text-text-muted">
            SIH 2026 &middot; Problem Statement: Mn Reserve Estimation
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  )
}