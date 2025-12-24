"""Configuration management for the insurance bot backend."""
from enum import Enum
from typing import Optional
from pydantic_settings import BaseSettings


class ModelProvider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    OLLAMA = "ollama"
    LMSTUDIO = "lmstudio"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI settings
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"

    # Ollama settings
    ollama_model: str = "llama3.1"
    ollama_base_url: str = "http://localhost:11434"

    # LM Studio settings
    lmstudio_model: str = "local-model"
    lmstudio_base_url: str = "http://localhost:1234/v1"

    # Model provider selection
    model_provider: ModelProvider = ModelProvider.OPENAI

    # Redis settings
    redis_url: str = "redis://localhost:6379/0"

    # API settings (for Phase 2)
    api_base_url: Optional[str] = None
    api_token: Optional[str] = None

    # CORS settings
    cors_origins: str = "http://localhost:3000"

    def get_cors_origins(self) -> list[str]:
        return self.cors_origins.split(",")

    class Config:
        env_file = ".env"
        case_sensitive = False
        protected_namespaces = ('settings_',)


settings = Settings()

