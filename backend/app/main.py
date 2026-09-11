"""Travel Planner Agent - FastAPI backend."""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import chat, trips, weather

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Travel Planner Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "demo_mode": settings.demo_mode,
        "granite_provider": "ibm-granite"
        if (not settings.demo_mode and settings.granite_configured)
        else "mock-granite",
        "weather_source": "live" if settings.weather_configured else "demo",
    }


app.include_router(trips.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(weather.router, prefix="/api")
