"""Prompt templates sent to IBM Granite."""


def trip_planning_prompt(req, days: int) -> str:
    interests = ", ".join(req.interests) if req.interests else "General sightseeing"
    return f"""You are a professional travel planner. Create a practical, personalized travel plan.

Trip details:
- Origin: {req.origin}
- Destination: {req.destination}
- Duration: {days} days
- Travellers: {req.travellers}
- Budget: {req.currency} {req.budget:,.0f}
- Travel style: {req.travel_style}
- Interests: {interests}
- Additional preferences: {req.preferences or 'None'}

Return ONLY a valid JSON object (no markdown, no explanation) with exactly this structure:
{{
  "trip_summary": "2-3 sentence personalized summary",
  "estimated_budget": {{
    "transportation": 0, "accommodation": 0, "food": 0,
    "activities": 0, "local_transport": 0, "miscellaneous": 0, "total": 0
  }},
  "itinerary": [
    {{
      "day": 1, "title": "Day title",
      "activities": [
        {{"time": "10:00 AM", "activity": "Activity name", "location": "Place", "estimated_cost": 0}}
      ]
    }}
  ],
  "accommodation": [
    {{"name": "Name", "type": "Budget/Standard/Premium", "estimated_price_per_night": 0, "location": "Area", "why": "Why it suits this trip"}}
  ],
  "transportation": [
    {{"mode": "Train/Flight/Bus", "description": "Short description", "estimated_cost": 0}}
  ],
  "tips": ["tip 1", "tip 2", "tip 3", "tip 4", "tip 5"]
}}

Rules:
- The itinerary must have exactly {days} days.
- All costs are per total trip (not per person) in {req.currency}.
- The estimated total should be close to but not above the budget of {req.budget:,.0f} if possible.
- Provide 3 accommodation options (Budget, Standard, Premium) and 2-3 transport options.
- Provide 5-8 practical travel tips.
JSON:"""


def chat_prompt(req, plan_json: str, question: str) -> str:
    return f"""You are a helpful travel assistant. The user has the following travel plan:

{plan_json}

Trip request context: origin={req.origin}, destination={req.destination}, travellers={req.travellers}, budget={req.currency} {req.budget:,.0f}, style={req.travel_style}.

The user asks: "{question}"

Answer helpfully and concisely in 2-5 sentences. Refer to the actual plan details. Do not use markdown formatting."""


def replan_prompt(req, plan_json: str, instruction: str) -> str:
    return f"""You are a travel planner agent. Here is the current travel plan:

{plan_json}

Trip request context: origin={req.origin}, destination={req.destination}, travellers={req.travellers}, budget={req.currency} {req.budget:,.0f}, style={req.travel_style}.

The user wants to modify the trip: "{instruction}"

Return the UPDATED full plan as ONLY a valid JSON object with the exact same structure as the input plan (trip_summary, estimated_budget, itinerary, accommodation, transportation, tips), applying the requested change. Keep unchanged parts mostly the same. No markdown, no explanation, only JSON."""


def savings_prompt(req, plan_json: str) -> str:
    return f"""The user's estimated trip cost exceeds their budget.

Plan: {plan_json}
Budget: {req.currency} {req.budget:,.0f}

Give 3 simple, specific cost-saving suggestions for this trip. Return ONLY a JSON object:
{{"suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"]}}"""
