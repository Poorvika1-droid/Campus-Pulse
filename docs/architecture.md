# Quantix Architecture (v1)

## Data Flow

1. Clients request map and recommendation APIs.
2. Backend `CampusEngine` maintains in-memory location state.
3. `tick()` simulates occupancy changes every 3 seconds.
4. WebSocket streams snapshots to connected clients.
5. Recommendation and assistant layers consume same state.

## Components

- **Frontend (React):** dashboard, map panel, assistant, recommendation cards.
- **Backend (FastAPI):** API + websocket + decision engine.
- **Engine Layer:** crowd classification, queue estimate, predictive hints.

## Privacy Baseline

- No user identity required for occupancy insights.
- Crowd-level analytics based on aggregate counts.
- Optional social/friend features should be opt-in in future versions.
