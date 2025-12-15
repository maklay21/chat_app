from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_STR: str = "/api/v1"
    PROJECT_NAME: str
    ENVIRONMENT: Literal["local", "production"] = "local"
    
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str 

settings = Settings()
