from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MCP Services"

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    OWNER_TELEGRAM_ID: int

    LLM_API_KEY: str
    LLM_BASE_URL: str = "https://api.koboillm.com/v1"
    CHAT_MODEL: str
    MCP_SERVER_URL: str = "http://127.0.0.1:8000/mcp"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()