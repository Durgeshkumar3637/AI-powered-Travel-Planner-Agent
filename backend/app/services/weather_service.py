"""Weather service: OpenWeather API with a demo-data fallback."""
import logging
import random

import requests

from app.config import settings

logger = logging.getLogger("weather")

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(destination: str) -> dict:
    """Return current weather for a destination.

    Uses OpenWeather when WEATHER_API_KEY is configured; otherwise
    returns clearly-labelled demo data.
    """
    if settings.weather_configured:
        try:
            resp = requests.get(
                WEATHER_URL,
                params={"q": destination, "appid": settings.weather_api_key, "units": "metric"},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "source": "live",
                "destination": destination,
                "temperature": round(data["main"]["temp"]),
                "condition": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "rain_probability": _rain_probability(data),
            }
        except Exception as exc:  # noqa: BLE001
            logger.warning("Weather API failed: %s; using demo data.", exc)
    return demo_weather(destination)


def demo_weather(destination: str) -> dict:
    random.seed(hash(destination) % (2**32))
    return {
        "source": "demo",
        "destination": destination,
        "temperature": random.randint(22, 34),
        "condition": random.choice(
            ["Partly Cloudy", "Sunny", "Light Rain", "Pleasant", "Humid"]
        ),
        "humidity": random.randint(40, 85),
        "rain_probability": random.randint(0, 60),
    }


def _rain_probability(data: dict) -> int:
    return int(data.get("rain", {}).get("1h", 0) * 100)
