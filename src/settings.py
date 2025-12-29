from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Reads .env if present; ignores extra env vars
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_key: str = Field(default="change-me", validation_alias="API_KEY")
    database_url: str = Field(default="sqlite:///./data/app.db", validation_alias="DATABASE_URL")

    # Logging
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    log_file: str = Field(default="./logs/app.log", validation_alias="LOG_FILE")


def ensure_log_directory(log_file: str) -> None:
    """Create the parent directory for the log file if needed."""
    path = Path(log_file)
    if path.parent:
        path.parent.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    return Settings()
