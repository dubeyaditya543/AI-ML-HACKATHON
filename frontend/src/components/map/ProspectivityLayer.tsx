import { CircleMarker, Popup } from 'react-leaflet'
import type { ProspectivityCell } from '../../types'

function scoreColor(score: number): string {
  if (score > 75) return '#C97B2E' // ore accent — high prospectivity
  if (score > 50) return '#4FA3A8' // geo accent — moderate
  return '#5C5F4F' // muted — low priority
}

export default function ProspectivityLayer({ cells }: { cells: ProspectivityCell[] }) {
  return (
    <>
      {cells.map((cell) => (
        <CircleMarker
          key={cell.id}
          center={[cell.lat, cell.lng]}
          radius={6 + cell.prospectivityScore / 12}
          pathOptions={{
            color: scoreColor(cell.prospectivityScore),
            fillColor: scoreColor(cell.prospectivityScore),
            fillOpacity: 0.55,
            weight: 1.5,
          }}
        >
          <Popup>
            <div className="font-mono text-xs space-y-1">
              <p><strong>Prospectivity:</strong> {cell.prospectivityScore}%</p>
              <p><strong>Confidence:</strong> {cell.confidence}%</p>
              <p><strong>Predicted Grade:</strong> {cell.predictedGrade}%</p>
              <p><strong>Recommended:</strong> {cell.recommendedAction}</p>
            </div>
          </Popup>
        </CircleMarker>
      ))}
    </>
  )
}