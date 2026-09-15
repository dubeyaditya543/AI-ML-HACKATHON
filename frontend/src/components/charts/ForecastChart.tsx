import {
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts'
import type { ForecastPoint } from '../../types'

export default function ForecastChart({ data }: { data: ForecastPoint[] }) {
  return (
    <ResponsiveContainer width="100%" height={360}>
      <ComposedChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#33362B" />
        <XAxis
          dataKey="date"
          tick={{ fill: '#8A8C7F', fontSize: 11, fontFamily: 'JetBrains Mono' }}
          tickFormatter={(d: string) => d.slice(5)}
          interval={4}
        />
        <YAxis
          tick={{ fill: '#8A8C7F', fontSize: 11, fontFamily: 'JetBrains Mono' }}
          width={50}
        />
        <Tooltip
          contentStyle={{
            background: '#1B1D17',
            border: '1px solid #33362B',
            borderRadius: 2,
            fontFamily: 'JetBrains Mono',
            fontSize: 12,
          }}
          labelStyle={{ color: '#EDEAE0' }}
        />
        <Legend wrapperStyle={{ fontSize: 12, fontFamily: 'Space Grotesk' }} />
        <ReferenceLine y={data[0]?.target} stroke="#7A9B5C" strokeDasharray="4 4" label={{ value: 'Target', fill: '#7A9B5C', fontSize: 11 }} />
        <Area
          type="monotone"
          dataKey="actual"
          name="Actual"
          stroke="#EDEAE0"
          fill="#EDEAE0"
          fillOpacity={0.08}
          strokeWidth={2}
          connectNulls={false}
        />
        <Line
          type="monotone"
          dataKey="forecast"
          name="Forecast"
          stroke="#C97B2E"
          strokeWidth={2}
          strokeDasharray="5 3"
          dot={false}
        />
      </ComposedChart>
    </ResponsiveContainer>
  )
}