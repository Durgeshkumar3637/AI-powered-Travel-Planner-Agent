"""Granite provider abstraction.

GraniteProvider
       |
       +--- IBMGraniteProvider   (real IBM watsonx.ai / Granite)
       +--- MockGraniteProvider  (demo fallback)
"""
import json
import logging
import re

import requests

from app.ai.mock_granite import MockGraniteProvider
from app.config import settings

logger = logging.getLogger("granite")

IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"


class GraniteProvider:
    name = "base"

    def generate_text(self, prompt: str) -> str:
        raise NotImplementedError


class IBMGraniteProvider(GraniteProvider):
    """Calls IBM Granite models through the IBM watsonx.ai REST API."""

    name = "ibm-granite"

    def __init__(self):
        self._token = None

    def _get_token(self) -> str:
        if self._token:
            return self._token
        resp = requests.post(
            IAM_TOKEN_URL,
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": settings.ibm_cloud_api_key,
            },
            headers={"Accept": "application/json"},
            timeout=30,
        )
        resp.raise_for_status()
        self._token = resp.json()["access_token"]
        return self._token

    def generate_text(self, prompt: str) -> str:
        payload = {
            "input": prompt,
            "model_id": settings.granite_model_id,
            "project_id": settings.watsonx_project_id,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 2500,
                "min_new_tokens": 200,
                "temperature": 0.4,
            },
        }
        headers = {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        resp = requests.post(
            f"{settings.watsonx_url}/ml/v1/text/generation?version=2024-05-31",
            json=payload,
            headers=headers,
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["results"][0]["generated_text"]


def extract_json(text) -> dict:
    """Best-effort extraction of a JSON object from model output."""
    if isinstance(text, dict):
        return text
    text = text.strip()
    # strip markdown fences
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.DOTALL)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # take the outermost {...} block
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        return json.loads(match.group(0))
    raise ValueError("No valid JSON found in model output")


def get_provider() -> GraniteProvider:
    """Return the configured Granite provider.

    IBM Granite is the primary AI model. The mock provider is only a
    fallback used in demo mode or when IBM credentials are unavailable.
    """
    if not settings.demo_mode and settings.granite_configured:
        return IBMGraniteProvider()
    if not settings.demo_mode and not settings.granite_configured:
        logger.warning("IBM Granite credentials missing; falling back to mock provider.")
    return MockGraniteProvider()


def generate_json(prompt: str, fallback_factory=None) -> dict:
    """Generate JSON from Granite with validation, one retry, and fallback."""
    provider = get_provider()
    # The mock provider is context-free; use the caller's rich fallback data instead.
    if provider.name == "mock-granite" and fallback_factory is not None:
        return fallback_factory()
    last_error = None
    for attempt in range(2):
        try:
            return extract_json(provider.generate_text(prompt))
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            logger.warning("Granite attempt %s failed: %s", attempt + 1, exc)
    if settings.demo_mode or fallback_factory is not None:
        logger.warning("Granite failed (%s); using fallback data.", last_error)
        return fallback_factory() if fallback_factory else MockGraniteProvider().sample_trip({})
    raise RuntimeError("Unable to generate a valid AI response. Please try again.")


def generate_text(prompt: str, fallback: str = "") -> str:
    provider = get_provider()
    try:
        return provider.generate_text(prompt).strip()
    except Exception as exc:  # noqa: BLE001
        logger.warning("Granite text generation failed: %s", exc)
        if fallback:
            return fallback
        raise RuntimeError("Unable to get an AI response right now. Please try again.")
