"""Chat service for orchestrating conversational interactions."""
from backend.agent.agent_factory import create_agent_executor
from backend.memory.redis import get_memory
from backend.config import settings
import logging

logger = logging.getLogger(__name__)


class ChatService:
    """Service for managing chat interactions with the AI agent."""
    
    @staticmethod
    async def process_message(session_id: str, message: str) -> str:
        """
        Process a chat message and return the agent's response.
        
        Args:
            session_id: Unique session identifier
            message: User message
            
        Returns:
            Agent response as string
        """
        try:
            # Get memory for this session
            memory = get_memory(session_id, settings.redis_url)
            
            # Create agent executor for this session
            agent_executor = create_agent_executor(session_id)
            
            # Get current chat history (previous messages, not including current)
            chat_history = memory.messages
            
            # Invoke agent with current message and history
            result = await agent_executor.ainvoke({
                "input": message,
                "chat_history": chat_history,
            })
            
            response = result.get(
                "output",
                "I apologize, but I couldn't generate a response."
            )
            
            # Add both user message and assistant response to memory for persistence
            memory.add_user_message(message)
            memory.add_ai_message(response)
            
            return response
        
        except Exception as e:
            logger.error(f"Error in chat service: {e}", exc_info=True)
            error_msg = f"I encountered an error while processing your request: {str(e)}"
            
            # Try to add error message to memory if memory is available
            try:
                memory = get_memory(session_id, settings.redis_url)
                memory.add_ai_message(error_msg)
            except Exception:
                # If memory fails, log but don't fail the request
                logger.warning(f"Failed to add error message to memory: {e}")
            
            return error_msg


