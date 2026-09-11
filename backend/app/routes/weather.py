"""Weather endpoint."""
from fastapi import APIRouter, HTTPException

from app.services import weather_service

router = APIRouter()


@router.get("/weather")
def get_weather(destination: str = "Goa"):
    if not destination.strip():
        raise HTTPException(status_code=400, detail="Destination is required.")
    try:
        return weather_service.get_weather(destination.strip())
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=502, detail="Unable to fetch weather right now."
        ) from exc
