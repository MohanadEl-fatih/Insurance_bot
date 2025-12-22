"""Chat API request/response schemas."""
from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    sid: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    message: str
    meta: Optional[dict] = None

