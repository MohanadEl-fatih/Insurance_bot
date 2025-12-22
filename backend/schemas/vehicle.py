"""Vehicle data models."""
from pydantic import BaseModel
from typing import Optional


class Vehicle(BaseModel):
    """Canonical vehicle model."""
    vin: Optional[str] = None
    make: str
    model: str
    year: int

