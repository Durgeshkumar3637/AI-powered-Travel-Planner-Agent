"""Trip planning endpoints: /api/plan-trip and /api/replan-trip."""
import json
from datetime import date, datetime

from fastapi import APIRouter, HTTPException

from app.ai import granite_client, prompts
from app.ai.mock_granite import MockGraniteProvider
from app.models.trip_models import (
    ReplanRequest,
    SavingsSuggestions,
    TripPlan,
    TripRequest,
)

router = APIRouter()


def compute_days(req: TripRequest) -> int:
    try:
        start = datetime.strptime(req.start_date, "%Y-%m-%d").date()
        end = datetime.strptime(req.end_date, "%Y-%m-%d").date()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid dates. Please use YYYY-MM-DD.") from exc
    if end < start:
        raise HTTPException(status_code=400, detail="End date must be after the start date.")
    days = (end - start).days + 1
    if days < 1 or days > 30:
        raise HTTPException(status_code=400, detail="Trip duration must be between 1 and 30 days.")
    return days


def validate_and_fix(plan_data: dict, days: int) -> dict:
    """Basic programmatic fixes on top of the AI output."""
    budget = plan_data.setdefault("estimated_budget", {})
    for key in (
        "transportation", "accommodation", "food",
        "activities", "local_transport", "miscellaneous", "total",
    ):
        try:
            budget[key] = float(budget.get(key, 0))
        except (TypeError, ValueError):
            budget[key] = 0.0
    # always recompute the total in Python (never trust the LLM's math)
    budget["total"] = sum(
        v for k, v in budget.items() if k != "total"
    )
    if not plan_data.get("itinerary"):
        raise ValueError("Empty itinerary")
    return plan_data


def fallback_trip(req: TripRequest, days: int) -> dict:
    return MockGraniteProvider().sample_trip({
        "origin": req.origin,
        "destination": req.destination,
        "days": days,
        "travellers": req.travellers,
        "travel_style": req.travel_style,
        "interests": req.interests,
        "currency": req.currency,
        "budget": req.budget,
    })


def build_plan(req: TripRequest) -> dict:
    days = compute_days(req)
    prompt = prompts.trip_planning_prompt(req, days)
    plan_data = granite_client.generate_json(
        prompt, fallback_factory=lambda: fallback_trip(req, days)
    )
    try:
        plan_data = validate_and_fix(plan_data, days)
        plan = TripPlan.model_validate(plan_data)
    except Exception:  # noqa: BLE001
        plan_data = fallback_trip(req, days)
        plan = TripPlan.model_validate(plan_data)

    result = {
        "plan": plan.model_dump(),
        "days": days,
        "over_budget": plan.estimated_budget.total > req.budget > 0,
        "remaining": req.budget - plan.estimated_budget.total,
        "provider": granite_client.get_provider().name,
        "trip_request": req.model_dump(),
    }
    if result["over_budget"]:
        result["savings_suggestions"] = _savings_suggestions(req, plan)
    return result


def _savings_suggestions(req: TripRequest, plan: TripPlan) -> list:
    prompt = prompts.savings_prompt(req, json.dumps(plan.model_dump()))
    try:
        data = granite_client.generate_json(prompt)
        return SavingsSuggestions.model_validate(data).suggestions
    except Exception:  # noqa: BLE001
        return [
            "Switch to budget accommodation to save on stay costs.",
            "Replace one paid activity with a free beach or market visit.",
            "Use local buses or rental scooters instead of taxis.",
        ]


@router.post("/plan-trip")
def plan_trip(req: TripRequest):
    try:
        if not req.destination.strip():
            raise HTTPException(status_code=400, detail="Destination is required.")
        return build_plan(req)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=502,
            detail="Unable to generate your trip right now. Please try again.",
        ) from exc


@router.post("/replan-trip")
def replan_trip(req: ReplanRequest):
    try:
        plan_json = json.dumps(req.trip.model_dump())
        prompt = prompts.replan_prompt(req.trip_request, plan_json, req.instruction)
        days = len(req.trip.itinerary) or 1
        plan_data = granite_client.generate_json(
            prompt,
            fallback_factory=lambda: _mock_replan(req),
        )
        plan_data = validate_and_fix(plan_data, days)
        plan = TripPlan.model_validate(plan_data)
        budget = req.trip_request.budget
        return {
            "plan": plan.model_dump(),
            "days": len(plan.itinerary),
            "over_budget": plan.estimated_budget.total > budget > 0,
            "remaining": budget - plan.estimated_budget.total,
            "provider": granite_client.get_provider().name,
            "trip_request": req.trip_request.model_dump(),
            "change_applied": req.instruction,
        }
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=502,
            detail="Unable to modify your trip right now. Please try again.",
        ) from exc


def _mock_replan(req: ReplanRequest) -> dict:
    provider = MockGraniteProvider()
    prompt = (
        f'modify the trip: "{req.instruction}"\n'
        + json.dumps(req.trip.model_dump())
    )
    return json.loads(provider.generate_text(prompt))
