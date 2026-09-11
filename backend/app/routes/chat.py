"""Simple AI chat endpoint that keeps the current trip as context."""
import json

from fastapi import APIRouter, HTTPException

from app.ai import granite_client, prompts
from app.models.trip_models import ChatRequest

router = APIRouter()


@router.post("/chat")
def chat(req: ChatRequest):
    plan_json = json.dumps(req.trip.model_dump())
    prompt = prompts.chat_prompt(req.trip_request, plan_json, req.question)
    fallback = (
        "Based on your current plan, you can reduce your estimated cost by choosing "
        "budget accommodation and replacing one paid activity with a free visit to a "
        "beach or local market. Using local buses instead of taxis also saves money."
    )
    try:
        answer = granite_client.generate_text(prompt, fallback=fallback)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=502, detail="The AI assistant is unavailable right now. Please try again."
        ) from exc
    return {"answer": answer, "provider": granite_client.get_provider().name}
