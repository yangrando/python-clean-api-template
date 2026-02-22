from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "python-clean-api-template"
    environment: str = Field(default="development", pattern="^(development|staging|production)$")
    log_level: str = "INFO"

    # Keep startup resilient in development/test; enforce strong keys at app boot for production.
    secret_key: str = "change-this-secret-key-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=60, ge=1)

    llm_provider: str = Field(default="fake", pattern="^(fake|openai_stub)$")
    openai_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
