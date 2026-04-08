import { LocationSnapshot } from '../types'

const levelColor: Record<string, string> = {
  low: '#22c55e',
  medium: '#f59e0b',
  high: '#ef4444',
}

interface Props {
  points: LocationSnapshot[]
}

export function MapPanel({ points }: Props) {
  return (
    <section className="card">
      <h2>Live Campus Map</h2>
      <div className="map-box">
        {points.map((point) => (
          <button
            key={point.location.id}
            className="pin"
            title={`${point.location.name} • ${point.crowd_level}`}
            style={{ left: `${point.location.x}%`, top: `${point.location.y}%`, background: levelColor[point.crowd_level] }}
          >
            {point.location.name.slice(0, 2).toUpperCase()}
          </button>
        ))}
      </div>
      <div className="list">
        {points.map((point) => (
          <article key={point.location.id} className="list-item">
            <strong>{point.location.name}</strong>
            <span>{point.crowd_level.toUpperCase()} • {point.availability_pct}% free</span>
            {point.wait_time_mins !== null && <span>Queue: {point.wait_time_mins} mins</span>}
          </article>
        ))}
      </div>
    </section>
  )
}
