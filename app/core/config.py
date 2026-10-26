from pathlib import Path
from typing import ClassVar
from urllib.parse import urlsplit

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

base_dir = Path(__file__).resolve().parent.parent.parent


class AppSettings(BaseSettings):
    APP_NAME: str = "Schema-Guard-API"
    APP_STAGE: str = Field(default="development", min_length=3, max_length=20)
    DIRECT_URL: str = Field(default=..., min_length=3)
    DATABASE_URL: str = Field(default=..., min_length=3)
    GITHUB_CLIENT_ID: str = Field(default=..., min_length=3)
    GITHUB_CLIENT_SECRET: str = Field(default=..., min_length=3)
    API_ORIGIN: str = Field(default="http://localhost:8000", min_length=1)
    SESSION_SECRET: str = Field(default=..., min_length=3)
    FRONTEND_ORIGIN: str = Field(default="http://localhost:3000", min_length=1)

    @field_validator("API_ORIGIN")
    @classmethod
    def validate_api_origin(cls, value: str) -> str:
        origin = urlsplit(value)
        if (
            origin.scheme not in {"http", "https"}
            or not origin.netloc
            or origin.username
            or origin.password
            or origin.path not in {"", "/"}
            or origin.query
            or origin.fragment
        ):
            raise ValueError("API_ORIGIN must be an HTTP(S) origin without a path.")
        try:
            origin.port
        except ValueError as error:
            raise ValueError("API_ORIGIN must have a valid port.") from error
        return value.rstrip("/")

    @field_validator("FRONTEND_ORIGIN")
    @classmethod
    def validate_frontend_origin(cls, value: str) -> str:
        origin = urlsplit(value)
        if (
            origin.scheme not in {"http", "https"}
            or not origin.netloc
            or origin.username
            or origin.password
            or origin.path not in {"", "/"}
            or origin.query
            or origin.fragment
        ):
            raise ValueError("FRONTEND_ORIGIN must be an HTTP(S) origin without a path.")
        try:
            origin.port
        except ValueError as error:
            raise ValueError("FRONTEND_ORIGIN must have a valid port.") from error
        return value.rstrip("/")

    @property
    def github_callback_url(self) -> str:
        return f"{self.API_ORIGIN}/api/v1/auth/github/callback"

    @property
    def is_production(self) -> bool:
        return self.APP_STAGE.lower() == "production"

    @model_validator(mode="after")
    def require_https_in_production(self) -> "AppSettings":
        if self.is_production and any(
            urlsplit(origin).scheme != "https"
            for origin in (self.API_ORIGIN, self.FRONTEND_ORIGIN)
        ):
            raise ValueError("API_ORIGIN and FRONTEND_ORIGIN must use HTTPS in production.")
        return self

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=f"{base_dir}/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings: AppSettings = AppSettings()