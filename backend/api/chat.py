"""Chat API endpoint."""
from fastapi import APIRouter, Cookie, Response
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.services.chat_service import ChatService
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    response: Response,
    sid: str = Cookie(None)
):
    """
    Handle chat messages. Returns sync JSON response.
    
    Creates or uses existing session ID via cookie.
    """
    # Generate or use existing session ID
    session_id = sid or str(uuid.uuid4())
    
    # Set session cookie if not present
    if not sid:
        response.set_cookie(
            key="sid",
            value=session_id,
            httponly=True,
            samesite="lax",
            max_age=86400,  # 24 hours
        )
    
    try:
        # Use service layer to process message
        reply = await ChatService.process_message(session_id, request.message)
        
        return ChatResponse(
            message=reply,
            meta={"session_id": session_id}
        )
    
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        return ChatResponse(
            message="I'm sorry, I encountered an error. Please try again.",
            meta={"error": str(e)}
        )

