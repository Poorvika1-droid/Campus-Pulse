from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Literal

from pydantic import BaseModel, Field


class CrowdLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class LocationType(str, Enum):
    library = "library"
    canteen = "canteen"
    lab = "lab"
    classroom = "classroom"
    event = "event"
    common = "common"


class Location(BaseModel):
    id: str
    name: str
    type: LocationType
    x: float = Field(ge=0, le=100)
    y: float = Field(ge=0, le=100)
    capacity: int = Field(gt=0)
    occupancy: int = Field(ge=0)
    activity: str


class LocationSnapshot(BaseModel):
    location: Location
    crowd_level: CrowdLevel
    availability_pct: int
    wait_time_mins: int | None = None


class Event(BaseModel):
    id: str
    title: str
    venue_id: str
    starts_at: datetime
    ends_at: datetime
    category: str
    attendees: int = 0


class AskRequest(BaseModel):
    question: str
    user_context: Dict[str, str] | None = None


class AskResponse(BaseModel):
    answer: str
    suggestions: List[str] = Field(default_factory=list)


class RecommendationResponse(BaseModel):
    study_spot: str
    food_spot: str
    event_pick: str
    reason: str


class DashboardStats(BaseModel):
    study_minutes_today: int
    movement_score: int = Field(ge=0, le=100)
    focus_score: int = Field(ge=0, le=100)
    crowd_exposure: Literal["low", "moderate", "high"]
