"""Configuration management for the insurance bot backend."""
import os
from enum import Enum
from typing import Optional
from pydantic_settings import BaseSettings


class ModelProvider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    OLLAMA = "ollama"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI settings
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # Ollama settings
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Model provider selection
    model_provider: ModelProvider = ModelProvider(
        os.getenv("MODEL_PROVIDER", "openai").lower()
    )
    
    # Redis settings
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # API settings (for Phase 2)
    api_base_url: Optional[str] = os.getenv("API_BASE_URL")
    api_token: Optional[str] = os.getenv("API_TOKEN")
    
    # CORS settings
    cors_origins: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000"
    ).split(",")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

