# Quantix – AI-Powered Real-Time Campus Intelligence System

Quantix is a full-stack smart-campus platform that provides live crowd intelligence, canteen queue prediction, study spot recommendations, event pulse visibility, and an AI assistant for campus decisions.

## Monorepo Structure

- `backend/` – FastAPI service with live simulation, recommendations, assistant API, websocket stream.
- `frontend/` – React + Vite dashboard with live campus map and AI interaction.
- `docs/` – product docs and architecture notes.

## Features Implemented

- Live Campus Map with occupancy and crowd levels.
- Crowd Intelligence (low/medium/high by area).
- Smart Canteen Queue estimation.
- Study Spot Finder recommendation.
- Event Pulse feed.
- AI Campus Assistant API + chat UI.
- Killer feature endpoint: "Where Should I Go Now?"
- Predictive message for next crowd trend.
- Personal productivity dashboard.
- Privacy-first architecture baseline (anonymous occupancy simulation).

## Run Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API base: `http://localhost:8000`

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

Set custom API URL if needed:

```bash
VITE_API_URL=http://localhost:8000 npm run dev
```

## Key API Endpoints

- `GET /health`
- `GET /api/map`
- `GET /api/events`
- `GET /api/recommendations`
- `POST /api/assistant`
- `GET /api/dashboard`
- `WS /ws/live`

## Next Steps

- Replace simulated occupancy with real sensor/check-in streams.
- Add authentication + role-based admin views.
- Integrate map provider (Mapbox) with actual campus tiles.
- Add multi-campus tenancy.
