"""LLM provider factory for OpenAI, Ollama, and LM Studio."""
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from config import settings, ModelProvider
import logging

logger = logging.getLogger(__name__)


def get_llm() -> BaseChatModel:
    """
    Create LLM instance based on configured provider.

    Returns:
        BaseChatModel instance (ChatOpenAI or compatible wrapper)
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
        return ChatOpenAI(
            model=settings.ollama_model,
            base_url=f"{settings.ollama_base_url}/v1",
            api_key="ollama",
            temperature=0.7,
        )

    elif settings.model_provider == ModelProvider.LMSTUDIO:
        logger.info(f"Initializing LM Studio model: {settings.lmstudio_model}")
        return ChatOpenAI(
            model=settings.lmstudio_model,
            base_url=settings.lmstudio_base_url,
            api_key="lm-studio",  # LM Studio doesn't require real API key
            temperature=0.7,
        )

    else:
        raise ValueError(f"Unsupported model provider: {settings.model_provider}")

