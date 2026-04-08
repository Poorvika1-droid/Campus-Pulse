import { DashboardStats } from '../types'

interface Props {
  stats: DashboardStats | null
}

export function DashboardPanel({ stats }: Props) {
  return (
    <section className="card">
      <h2>Personal Productivity</h2>
      {!stats ? (
        <p>Loading dashboard...</p>
      ) : (
        <div className="metrics">
          <article><span>Study Time</span><strong>{stats.study_minutes_today} mins</strong></article>
          <article><span>Movement Score</span><strong>{stats.movement_score}/100</strong></article>
          <article><span>Focus Score</span><strong>{stats.focus_score}/100</strong></article>
          <article><span>Crowd Exposure</span><strong>{stats.crowd_exposure}</strong></article>
        </div>
      )}
    </section>
  )
}
