"""Backend API tests - all pass in DEMO_MODE (default)."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

TRIP = {
    "origin": "Delhi",
    "destination": "Goa",
    "start_date": "2026-10-10",
    "end_date": "2026-10-14",
    "travellers": 2,
    "budget": 40000,
    "currency": "INR",
    "travel_style": "Couple",
    "interests": ["Beaches", "Food", "Sightseeing"],
    "preferences": "Relaxed trip",
}


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_plan_trip():
    r = client.post("/api/plan-trip", json=TRIP)
    assert r.status_code == 200
    data = r.json()
    assert data["days"] == 5
    plan = data["plan"]
    assert len(plan["itinerary"]) == 5
    assert plan["estimated_budget"]["total"] > 0
    assert len(plan["tips"]) >= 5


def test_plan_trip_budget_total_is_recomputed():
    r = client.post("/api/plan-trip", json=TRIP)
    b = r.json()["plan"]["estimated_budget"]
    expected = sum(
        b[k] for k in ("transportation", "accommodation", "food",
                       "activities", "local_transport", "miscellaneous")
    )
    assert b["total"] == pytest.approx(expected)


def test_plan_trip_over_budget_returns_savings():
    trip = dict(TRIP, budget=100)
    r = client.post("/api/plan-trip", json=trip)
    assert r.status_code == 200
    data = r.json()
    assert data["over_budget"] is True
    assert len(data["savings_suggestions"]) >= 2


def test_missing_destination():
    trip = dict(TRIP, destination=" ")
    r = client.post("/api/plan-trip", json=trip)
    assert r.status_code == 400


def test_invalid_dates():
    r = client.post("/api/plan-trip", json=dict(TRIP, start_date="2026-10-14", end_date="2026-10-10"))
    assert r.status_code == 400


def test_negative_budget():
    r = client.post("/api/plan-trip", json=dict(TRIP, budget=-500))
    assert r.status_code == 422


def test_weather_demo():
    r = client.get("/api/weather", params={"destination": "Goa"})
    assert r.status_code == 200
    body = r.json()
    assert body["source"] in ("live", "demo")
    assert "temperature" in body


def test_chat():
    plan = client.post("/api/plan-trip", json=TRIP).json()["plan"]
    r = client.post("/api/chat", json={"question": "Make my trip cheaper.", "trip": plan, "trip_request": TRIP})
    assert r.status_code == 200
    assert len(r.json()["answer"]) > 10


def test_replan():
    result = client.post("/api/plan-trip", json=TRIP).json()
    r = client.post(
        "/api/replan-trip",
        json={
            "instruction": "Make Day 3 more relaxed.",
            "trip": result["plan"],
            "trip_request": TRIP,
        },
    )
    assert r.status_code == 200
    assert len(r.json()["plan"]["itinerary"]) == 5


def test_mock_granite_sample():
    from app.ai.mock_granite import MockGraniteProvider
    plan = MockGraniteProvider().sample_trip({"destination": "Goa", "days": 5})
    assert len(plan["itinerary"]) == 5
