from __future__ import annotations

import asyncio
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .engine import CampusEngine
from .models import AskRequest, AskResponse, DashboardStats, RecommendationResponse

app = FastAPI(title="Quantix API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = CampusEngine()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "quantix-api"}


@app.get("/api/map")
def get_map_data():
    return {"timestamp": datetime.utcnow(), "locations": [s.model_dump() for s in engine.snapshot()]}


@app.get("/api/events")
def get_events():
    return {"events": [e.model_dump() for e in engine.events]}


@app.get("/api/recommendations", response_model=RecommendationResponse)
def get_recommendations() -> RecommendationResponse:
    study = engine.find_best_study_spot()
    food = engine.find_best_food_spot()
    event = engine.next_event()
    event_text = event.title if event else "No active event right now"
    return RecommendationResponse(
        study_spot=study.location.name,
        food_spot=food.location.name,
        event_pick=event_text,
        reason=(
            f"{study.location.name} has {study.availability_pct}% availability. "
            f"{food.location.name} wait time is ~{food.wait_time_mins} mins. "
            f"Prediction: {engine.predict_peak_message()}"
        ),
    )


@app.post("/api/assistant", response_model=AskResponse)
def ask_assistant(payload: AskRequest) -> AskResponse:
    q = payload.question.lower()
    rec = get_recommendations()

    if "study" in q:
        return AskResponse(
            answer=f"Best study option now is {rec.study_spot}.",
            suggestions=["Open map", "Notify me if library gets free"],
        )
    if "eat" in q or "canteen" in q or "food" in q:
        return AskResponse(
            answer=f"Go to {rec.food_spot}. Estimated queue is low right now.",
            suggestions=["Show wait time trend", "Set lunch reminder"],
        )
    if "event" in q:
        return AskResponse(
            answer=f"Recommended event: {rec.event_pick}",
            suggestions=["Add to calendar", "Get route"],
        )

    return AskResponse(
        answer=(
            "I can help with crowd levels, study spot recommendations, canteen queues, and live events. "
            f"If you're deciding quickly, try: {rec.study_spot} for study and {rec.food_spot} for food."
        ),
        suggestions=["Where should I go now?", "Least crowded area"],
    )


@app.get("/api/dashboard", response_model=DashboardStats)
def get_dashboard() -> DashboardStats:
    now = datetime.utcnow().hour
    study_minutes = 110 if now < 14 else 180
    return DashboardStats(
        study_minutes_today=study_minutes,
        movement_score=72,
        focus_score=78,
        crowd_exposure="moderate",
    )


@app.websocket("/ws/live")
async def ws_live(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            engine.tick()
            data = {"timestamp": datetime.utcnow().isoformat(), "locations": [s.model_dump() for s in engine.snapshot()]}
            await websocket.send_json(data)
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        return
