from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Dict, List

from .models import CrowdLevel, Event, Location, LocationSnapshot, LocationType


class CampusEngine:
    def __init__(self) -> None:
        self.locations: Dict[str, Location] = {
            "lib": Location(
                id="lib",
                name="Central Library",
                type=LocationType.library,
                x=20,
                y=30,
                capacity=240,
                occupancy=180,
                activity="Exam prep",
            ),
            "can": Location(
                id="can",
                name="Main Canteen",
                type=LocationType.canteen,
                x=68,
                y=52,
                capacity=180,
                occupancy=130,
                activity="Lunch service",
            ),
            "lab": Location(
                id="lab",
                name="Innovation Lab",
                type=LocationType.lab,
                x=34,
                y=65,
                capacity=80,
                occupancy=24,
                activity="Prototype work",
            ),
            "cblock": Location(
                id="cblock",
                name="C Block",
                type=LocationType.classroom,
                x=52,
                y=24,
                capacity=160,
                occupancy=56,
                activity="Open classrooms",
            ),
            "quad": Location(
                id="quad",
                name="Student Quad",
                type=LocationType.common,
                x=80,
                y=34,
                capacity=220,
                occupancy=95,
                activity="Break & social",
            ),
        }

        now = datetime.utcnow()
        self.events: List[Event] = [
            Event(
                id="e1",
                title="Hackathon Kickoff",
                venue_id="lab",
                starts_at=now + timedelta(minutes=25),
                ends_at=now + timedelta(hours=3),
                category="Tech",
                attendees=63,
            ),
            Event(
                id="e2",
                title="AI Seminar",
                venue_id="cblock",
                starts_at=now + timedelta(hours=1),
                ends_at=now + timedelta(hours=2),
                category="Academic",
                attendees=89,
            ),
        ]

    def _crowd_level(self, occupancy: int, capacity: int) -> CrowdLevel:
        ratio = occupancy / capacity
        if ratio < 0.4:
            return CrowdLevel.low
        if ratio < 0.75:
            return CrowdLevel.medium
        return CrowdLevel.high

    def snapshot(self) -> List[LocationSnapshot]:
        items: List[LocationSnapshot] = []
        for loc in self.locations.values():
            level = self._crowd_level(loc.occupancy, loc.capacity)
            availability_pct = max(0, int((1 - (loc.occupancy / loc.capacity)) * 100))
            wait_time = None
            if loc.type == LocationType.canteen:
                wait_time = int(max(2, (loc.occupancy / loc.capacity) * 24))
            items.append(
                LocationSnapshot(
                    location=loc,
                    crowd_level=level,
                    availability_pct=availability_pct,
                    wait_time_mins=wait_time,
                )
            )
        return items

    def tick(self) -> None:
        hour = datetime.utcnow().hour
        for loc in self.locations.values():
            drift = random.randint(-8, 12)
            if loc.type == LocationType.canteen and 12 <= hour <= 14:
                drift += random.randint(10, 24)
            if loc.type == LocationType.library and 16 <= hour <= 20:
                drift += random.randint(4, 16)
            loc.occupancy = max(0, min(loc.capacity, loc.occupancy + drift))

    def find_best_study_spot(self) -> LocationSnapshot:
        candidates = [
            s
            for s in self.snapshot()
            if s.location.type in {LocationType.library, LocationType.lab, LocationType.classroom}
        ]
        return max(candidates, key=lambda s: s.availability_pct)

    def find_best_food_spot(self) -> LocationSnapshot:
        candidates = [s for s in self.snapshot() if s.location.type == LocationType.canteen]
        return min(candidates, key=lambda s: s.wait_time_mins or 0)

    def next_event(self) -> Event | None:
        now = datetime.utcnow()
        upcoming = sorted([e for e in self.events if e.ends_at > now], key=lambda e: e.starts_at)
        return upcoming[0] if upcoming else None

    def predict_peak_message(self) -> str:
        hour = datetime.utcnow().hour
        if 11 <= hour <= 13:
            return "Canteen likely to be high-crowd around 1 PM."
        if 16 <= hour <= 18:
            return "Library crowd expected to rise after 5 PM."
        return "Campus load expected to stay moderate in the next 2 hours."

