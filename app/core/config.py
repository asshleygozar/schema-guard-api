from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import Field

base_dir = Path(__file__).resolve().parent.parent.parent


class AppSettings(BaseSettings):
    APP_NAME: str = "Schema-Guard-API"
    APP_STAGE: str = Field(default="development", min_length=3, max_length=20)
    DIRECT_URL: str = Field(default=..., min_length=3)
    DATABASE_URL: str = Field(default=...,min_length=3)
    @property
    def is_production(self) -> bool:
        return self.APP_STAGE.lower() == "production"

    model_config = SettingsConfigDict(
        env_file=f"{base_dir}/.env", env_file_encoding="utf-8", extra="ignore"
    )


settings = AppSettings()