"""Mock Granite provider used in DEMO_MODE or as an automatic fallback.

This lets the application be demonstrated without IBM credentials.
IBM Granite remains the primary AI model; this is only a demo substitute.
"""
from app.ai.prompts import trip_planning_prompt  # noqa: F401  (kept for parity)


class MockGraniteProvider:
    name = "mock-granite"

    def generate_text(self, prompt: str) -> str:
        # Very small rule-based "responses" for chat-style prompts.
        lower = prompt.lower()
        if "cost-saving suggestions" in lower or '"suggestions"' in lower:
            return (
                '{"suggestions": ['
                '"Switch to budget accommodation to save around 30% on stay costs.",'
                '"Replace one paid activity with a free beach or local market visit.",'
                '"Use local buses or a rental scooter instead of taxis for local transport."]}'
            )
        if "modify the trip" in lower:
            return self._replan_from_prompt(prompt)
        if "travel assistant" in lower:
            return (
                "Based on your current plan, you can reduce your estimated cost by choosing "
                "budget accommodation and replacing one paid activity with a free visit to a "
                "beach or local market. Using local buses instead of taxis also saves money, "
                "and travelling just outside peak season can lower accommodation prices."
            )
        return self.sample_trip({})

    # ------------------------------------------------------------------
    def _replan_from_prompt(self, prompt: str) -> str:
        import json
        import re

        plan_json = ""
        match = re.search(r"\{.*\}", prompt, flags=re.DOTALL)
        if match:
            plan_json = match.group(0)
        try:
            plan = json.loads(plan_json)
        except Exception:  # noqa: BLE001
            plan = self.sample_trip({})
        instruction = ""
        m = re.search(r'modify the trip:\s*"(.*)"', prompt, flags=re.DOTALL)
        if m:
            instruction = m.group(1).strip()
        lower = instruction.lower()
        if "relax" in lower and "day" in lower:
            day_num = next((int(d) for d in re.findall(r"\d+", instruction)), 3)
            for day in plan.get("itinerary", []):
                if day.get("day") == day_num:
                    day["title"] = "Relaxed " + day.get("title", "Day")
                    day["activities"] = day["activities"][:3]
            plan["trip_summary"] += " Day was relaxed per your request."
        elif "cheap" in lower or "budget" in lower or "cost" in lower:
            plan["estimated_budget"]["accommodation"] = int(
                plan["estimated_budget"]["accommodation"] * 0.7
            )
            plan["estimated_budget"]["activities"] = int(
                plan["estimated_budget"]["activities"] * 0.6
            )
            plan["estimated_budget"]["total"] = sum(
                v for k, v in plan["estimated_budget"].items() if k != "total"
            )
            plan["trip_summary"] += " The plan has been adjusted to reduce cost."
        return json.dumps(plan)

    # ------------------------------------------------------------------
    def sample_trip(self, ctx: dict) -> dict:
        destination = ctx.get("destination", "Goa")
        origin = ctx.get("origin", "Delhi")
        days = int(ctx.get("days", 5))
        travellers = int(ctx.get("travellers", 2))
        style = ctx.get("travel_style", "Standard")
        interests = ctx.get("interests", ["Beaches", "Food", "Sightseeing"])
        currency = ctx.get("currency", "INR")

        day_templates = [
            ("Arrival & First Look", [
                ("10:00 AM", f"Arrive in {destination} and check in", destination, 0),
                ("1:00 PM", "Lunch at a popular local restaurant", f"{destination}", 600),
                ("4:00 PM", "Relaxed walk around the main area", f"{destination}", 0),
                ("7:30 PM", "Dinner and local cuisine tasting", f"{destination}", 900),
            ]),
            ("Top Attractions", [
                ("9:00 AM", "Breakfast", "Hotel", 300),
                ("10:00 AM", "Visit the top-rated landmark", destination, 800),
                ("1:30 PM", "Lunch", destination, 600),
                ("3:30 PM", "Museum / heritage walk", destination, 500),
                ("7:30 PM", "Dinner", destination, 800),
            ]),
            ("Nature & Local Experiences", [
                ("8:30 AM", "Breakfast", "Hotel", 300),
                ("9:30 AM", "Scenic viewpoint / nature spot", destination, 600),
                ("1:00 PM", "Lunch", destination, 500),
                ("4:00 PM", "Local market exploration", destination, 0),
                ("7:00 PM", "Sunset spot", destination, 0),
            ]),
            ("Leisure Day", [
                ("9:00 AM", "Late breakfast", "Hotel", 350),
                ("11:00 AM", "Free time / optional activity", destination, 700),
                ("1:30 PM", "Lunch", destination, 600),
                ("5:00 PM", "Cafe hopping and shopping", destination, 400),
                ("8:00 PM", "Dinner", destination, 900),
            ]),
            ("Departure Day", [
                ("9:00 AM", "Breakfast and checkout", "Hotel", 300),
                ("11:00 AM", "Last-minute souvenir shopping", destination, 300),
                ("1:00 PM", "Lunch", destination, 500),
                ("3:00 PM", f"Depart for {origin}", destination, 0),
            ]),
        ]

        itinerary = []
        for i in range(days):
            title, acts = day_templates[i % len(day_templates)]
            itinerary.append({
                "day": i + 1,
                "title": title,
                "activities": [
                    {"time": t, "activity": a, "location": loc, "estimated_cost": c}
                    for t, a, loc, c in acts
                ],
            })

        per_person_food = 1200 if style != "Luxury" else 2500
        per_night_stay = {"Budget": 2000, "Standard": 3500, "Luxury": 7000}.get(style, 3000)
        food = per_person_food * days * travellers
        accommodation = per_night_stay * days * travellers
        activities = sum(
            a["estimated_cost"] for d in itinerary for a in d["activities"]
        ) * travellers
        transportation = 10000 if style != "Luxury" else 18000
        local_transport = 600 * days
        miscellaneous = 400 * days * travellers
        total = food + accommodation + activities + transportation + local_transport + miscellaneous
        budget = ctx.get("budget")
        if budget and budget >= 5000 and total > budget:
            # scale down so the sample plan fits the user's budget
            scale = (budget * 0.95) / total
            food, accommodation = int(food * scale), int(accommodation * scale)
            activities, transportation = int(activities * scale), int(transportation * scale)
            local_transport, miscellaneous = int(local_transport * scale), int(miscellaneous * scale)
            total = food + accommodation + activities + transportation + local_transport + miscellaneous

        return {
            "trip_summary": (
                f"A relaxed {days}-day trip to {destination} from {origin} for {travellers} "
                f"traveller(s), focused on {', '.join(interests).lower() if interests else 'sightseeing'}, "
                f"in a {style.lower()} style, designed to stay within your {currency} budget."
            ),
            "estimated_budget": {
                "transportation": transportation,
                "accommodation": accommodation,
                "food": food,
                "activities": activities,
                "local_transport": local_transport,
                "miscellaneous": miscellaneous,
                "total": total,
            },
            "itinerary": itinerary,
            "accommodation": [
                {
                    "name": f"Budget Stay near {destination} center",
                    "type": "Budget",
                    "estimated_price_per_night": 2000,
                    "location": destination,
                    "why": "Clean, affordable and close to main attractions.",
                },
                {
                    "name": f"Standard Hotel in {destination}",
                    "type": "Standard",
                    "estimated_price_per_night": 3500,
                    "location": destination,
                    "why": "Good balance of comfort, location and price.",
                },
                {
                    "name": f"Premium Resort, {destination}",
                    "type": "Premium",
                    "estimated_price_per_night": 7000,
                    "location": destination,
                    "why": "Great amenities and views for a special trip.",
                },
            ],
            "transportation": [
                {
                    "mode": "Train",
                    "description": f"Budget-friendly overnight option from {origin}",
                    "estimated_cost": 5000,
                },
                {
                    "mode": "Flight",
                    "description": f"Faster option from {origin}",
                    "estimated_cost": 9000,
                },
                {
                    "mode": "Local Transport",
                    "description": "Taxis, buses and rental scooters at the destination",
                    "estimated_cost": 3000,
                },
            ],
            "tips": [
                "Carry sunscreen and stay hydrated.",
                "Keep some cash for local transport and small vendors.",
                "Check attraction opening times before visiting.",
                "Carry comfortable footwear for walking.",
                "Keep emergency contact information handy.",
                "Book popular restaurants in advance during peak season.",
            ],
        }
