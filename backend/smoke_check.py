"""End-to-end smoke test against a running server (demo mode).
Usage: python smoke_check.py  (server must be running on port 8001)
"""
import json
import urllib.request

BASE = "http://localhost:8001"

REQ = {
    "origin": "Delhi", "destination": "Goa",
    "start_date": "2026-10-10", "end_date": "2026-10-14",
    "travellers": 2, "budget": 40000, "currency": "INR",
    "travel_style": "Couple", "interests": ["Beaches", "Food", "Sightseeing"],
    "preferences": "Relaxed trip",
}


def post(path, payload):
    r = urllib.request.urlopen(
        urllib.request.Request(BASE + path, json.dumps(payload).encode(),
                               {"Content-Type": "application/json"}))
    return json.load(r)


result = post("/api/plan-trip", REQ)
plan = result["plan"]
print(f"plan: days={result['days']} itinerary={len(plan['itinerary'])} "
      f"total={plan['estimated_budget']['total']} over_budget={result['over_budget']} "
      f"remaining={result['remaining']} provider={result['provider']}")

chat = post("/api/chat", {"question": "Make my trip cheaper.", "trip": plan, "trip_request": REQ})
print("chat:", chat["answer"][:120])

replan = post("/api/replan-trip", {"instruction": "Make Day 3 more relaxed.",
                                   "trip": plan, "trip_request": REQ})
print(f"replan: days={len(replan['plan']['itinerary'])} "
      f"day3='{replan['plan']['itinerary'][2]['title']}'")

assert len(plan["itinerary"]) == 5
assert not result["over_budget"]
print("SMOKE OK")
