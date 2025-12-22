"""Quote data models."""
from pydantic import BaseModel
from typing import Literal, Optional, Any


class Quote(BaseModel):
    """Canonical quote model."""
    provider: str
    premium_monthly: float
    coverage: Literal["liability", "comprehensive", "full"]
    details: Optional[dict[str, Any]] = None

