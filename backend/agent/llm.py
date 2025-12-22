"""LLM provider factory for OpenAI and Ollama."""
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_core.language_models import BaseChatModel
from backend.config import settings, ModelProvider
import logging

logger = logging.getLogger(__name__)


def get_llm() -> BaseChatModel:
    """
    Create LLM instance based on configured provider.
    
    Returns:
        BaseChatModel instance (ChatOpenAI or Ollama wrapper)
    """
    if settings.model_provider == ModelProvider.OPENAI:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY must be set when using OpenAI provider")
        
        logger.info(f"Initializing OpenAI model: {settings.openai_model}")
        return ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.7,
        )
    
    elif settings.model_provider == ModelProvider.OLLAMA:
        logger.info(f"Initializing Ollama model: {settings.ollama_model}")
        # Note: Ollama integration may need adjustment based on LangChain version
        # For now, using ChatOpenAI with Ollama's OpenAI-compatible endpoint
        return ChatOpenAI(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            api_key="ollama",  # Ollama doesn't require real API key
            temperature=0.7,
        )
    
    else:
        raise ValueError(f"Unsupported model provider: {settings.model_provider}")

