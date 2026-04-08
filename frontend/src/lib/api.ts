import { DashboardStats, LocationSnapshot, Recommendation } from '../types'

const API = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function getMapData(): Promise<LocationSnapshot[]> {
  const res = await fetch(`${API}/api/map`)
  const data = await res.json()
  return data.locations
}

export async function getRecommendations(): Promise<Recommendation> {
  const res = await fetch(`${API}/api/recommendations`)
  return res.json()
}

export async function askAssistant(question: string): Promise<{ answer: string; suggestions: string[] }> {
  const res = await fetch(`${API}/api/assistant`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  })
  return res.json()
}

export async function getDashboard(): Promise<DashboardStats> {
  const res = await fetch(`${API}/api/dashboard`)
  return res.json()
}

export function liveSocket(): WebSocket {
  return new WebSocket((API.replace('http', 'ws') + '/ws/live'))
}
