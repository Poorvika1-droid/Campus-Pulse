import { Recommendation } from '../types'

interface Props {
  recommendation: Recommendation | null
}

export function RecommendationPanel({ recommendation }: Props) {
  return (
    <section className="card">
      <h2>Where Should I Go Now?</h2>
      {!recommendation ? (
        <p>Loading recommendation...</p>
      ) : (
        <>
          <p><strong>Study:</strong> {recommendation.study_spot}</p>
          <p><strong>Food:</strong> {recommendation.food_spot}</p>
          <p><strong>Event:</strong> {recommendation.event_pick}</p>
          <p>{recommendation.reason}</p>
        </>
      )}
    </section>
  )
}
