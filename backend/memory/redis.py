"""Redis-backed conversation memory using LangChain."""
from langchain_community.chat_message_histories import RedisChatMessageHistory
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_memory(session_id: str, redis_url: str) -> RedisChatMessageHistory:
    """
    Get or create a Redis chat message history for a session.
    
    Args:
        session_id: Unique session identifier
        redis_url: Redis connection URL
        
    Returns:
        RedisChatMessageHistory instance
    """
    try:
        memory = RedisChatMessageHistory(
            session_id=f"session:{session_id}",
            url=redis_url,
            ttl=3600 * 24,  # 24 hours TTL
        )
        return memory
    except Exception as e:
        logger.error(f"Failed to create Redis memory for session {session_id}: {e}")
        raise

