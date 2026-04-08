export type CrowdLevel = 'low' | 'medium' | 'high'

export interface Location {
  id: string
  name: string
  type: 'library' | 'canteen' | 'lab' | 'classroom' | 'event' | 'common'
  x: number
  y: number
  capacity: number
  occupancy: number
  activity: string
}

export interface LocationSnapshot {
  location: Location
  crowd_level: CrowdLevel
  availability_pct: number
  wait_time_mins: number | null
}

export interface Recommendation {
  study_spot: string
  food_spot: string
  event_pick: string
  reason: string
}

export interface DashboardStats {
  study_minutes_today: number
  movement_score: number
  focus_score: number
  crowd_exposure: 'low' | 'moderate' | 'high'
}
