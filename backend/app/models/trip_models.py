"""Pydantic models for trip requests and validated AI responses."""
from typing import List, Optional
from pydantic import BaseModel, Field


class TripRequest(BaseModel):
    origin: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    start_date: str
    end_date: str
    travellers: int = Field(1, ge=1, le=20)
    budget: float = Field(0, ge=0)
    currency: str = "INR"
    travel_style: str = "Standard"
    interests: List[str] = []
    preferences: Optional[str] = ""


class Activity(BaseModel):
    time: str = " Flexible"
    activity: str
    location: str = ""
    estimated_cost: float = 0


class ItineraryDay(BaseModel):
    day: int
    title: str
    activities: List[Activity] = []


class BudgetBreakdown(BaseModel):
    transportation: float = 0
    accommodation: float = 0
    food: float = 0
    activities: float = 0
    local_transport: float = 0
    miscellaneous: float = 0
    total: float = 0


class AccommodationSuggestion(BaseModel):
    name: str
    type: str = "Standard"
    estimated_price_per_night: float = 0
    location: str = ""
    why: str = ""


class TransportSuggestion(BaseModel):
    mode: str
    description: str = ""
    estimated_cost: float = 0


class TripPlan(BaseModel):
    trip_summary: str
    estimated_budget: BudgetBreakdown
    itinerary: List[ItineraryDay]
    accommodation: List[AccommodationSuggestion] = []
    transportation: List[TransportSuggestion] = []
    tips: List[str] = []


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    trip: TripPlan
    trip_request: TripRequest


class ReplanRequest(BaseModel):
    instruction: str = Field(..., min_length=1)
    trip: TripPlan
    trip_request: TripRequest


class SavingsSuggestions(BaseModel):
    suggestions: List[str] = []
