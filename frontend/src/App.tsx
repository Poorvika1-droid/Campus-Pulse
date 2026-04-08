import { useEffect, useState } from 'react'
import { AssistantPanel } from './components/AssistantPanel'
import { DashboardPanel } from './components/DashboardPanel'
import { MapPanel } from './components/MapPanel'
import { RecommendationPanel } from './components/RecommendationPanel'
import { getDashboard, getMapData, getRecommendations, liveSocket } from './lib/api'
import { DashboardStats, LocationSnapshot, Recommendation } from './types'

export default function App() {
  const [points, setPoints] = useState<LocationSnapshot[]>([])
  const [recommendation, setRecommendation] = useState<Recommendation | null>(null)
  const [stats, setStats] = useState<DashboardStats | null>(null)

  useEffect(() => {
    getMapData().then(setPoints)
    getRecommendations().then(setRecommendation)
    getDashboard().then(setStats)

    const ws = liveSocket()
    ws.onmessage = (event) => {
      const payload = JSON.parse(event.data)
      setPoints(payload.locations)
    }

    return () => ws.close()
  }, [])

  return (
    <main className="layout">
      <header>
        <h1>QUANTIX</h1>
        <p>Know before you go.</p>
      </header>
      <div className="grid">
        <MapPanel points={points} />
        <RecommendationPanel recommendation={recommendation} />
        <AssistantPanel />
        <DashboardPanel stats={stats} />
      </div>
    </main>
  )
}
