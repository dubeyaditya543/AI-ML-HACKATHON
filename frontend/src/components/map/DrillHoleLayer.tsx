import { CircleMarker, Popup } from 'react-leaflet'
import type { DrillHole } from '../../types'

export default function DrillHoleLayer({ holes }: { holes: DrillHole[] }) {
  return (
    <>
      {holes.map((hole) => (
        <CircleMarker
          key={hole.id}
          center={[hole.lat, hole.lng]}
          radius={3}
          pathOptions={{ color: '#EDEAE0', fillColor: '#EDEAE0', fillOpacity: 0.8, weight: 1 }}
        >
          <Popup>
            <div className="font-mono text-xs space-y-1">
              <p><strong>{hole.id}</strong></p>
              <p>Depth: {hole.depth} m</p>
              <p>Mn Grade: {hole.mnGrade}%</p>
              <p>Rock: {hole.rockType}</p>
            </div>
          </Popup>
        </CircleMarker>
      ))}
    </>
  )
}