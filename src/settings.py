"""Settings module."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from enums import LogLevel


class Settings(BaseSettings):
    """Project settings."""

    model_config = SettingsConfigDict(env_file='settings.env', env_file_encoding='utf-8')

    PROXY_DOMAIN: str = '127.0.0.1'
    PROXY_PORT: int = '12334'

    LOG_LEVEL: LogLevel = LogLevel.INFO
    PORT: int = 8080


@lru_cache(1)
def get_settings() -> Settings:
    """Get project settings."""
    return Settings()
