import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell, ResponsiveContainer } from 'recharts'
import type { CauseContribution } from '../../types'

const BAR_COLORS = ['#C4432B', '#C97B2E', '#4FA3A8', '#8A8C7F', '#5C5F4F']

export default function CauseBreakdownChart({ causes }: { causes: CauseContribution[] }) {
  const sorted = [...causes].sort((a, b) => b.contributionPct - a.contributionPct)

  return (
    <ResponsiveContainer width="100%" height={sorted.length * 42 + 20}>
      <BarChart data={sorted} layout="vertical" margin={{ top: 4, right: 24, left: 8, bottom: 4 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#33362B" horizontal={false} />
        <XAxis
          type="number"
          domain={[0, 'dataMax + 5']}
          tick={{ fill: '#8A8C7F', fontSize: 11, fontFamily: 'JetBrains Mono' }}
          unit="%"
        />
        <YAxis
          type="category"
          dataKey="cause"
          width={140}
          tick={{ fill: '#EDEAE0', fontSize: 12, fontFamily: 'Space Grotesk' }}
        />
        <Tooltip
          contentStyle={{
            background: '#1B1D17',
            border: '1px solid #33362B',
            borderRadius: 2,
            fontFamily: 'JetBrains Mono',
            fontSize: 12,
          }}
          formatter={(value: number) => [`${value}%`, 'Contribution']}
        />
        <Bar dataKey="contributionPct" radius={[0, 2, 2, 0]}>
          {sorted.map((_, i) => (
            <Cell key={i} fill={BAR_COLORS[i % BAR_COLORS.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}