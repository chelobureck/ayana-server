from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_DEBUG: bool = True
    APP_CORS_ORIGINS: str = "*"

    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str
    OPENAI_MODEL: str
    OPENAI_TIMEOUT: int = 60

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "aitutor"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_TTL_SECONDS: int = 600

    FIREBASE_ENABLED: bool = False
    FIREBASE_PROJECT_ID: str | None = None

    # Google OAuth
    GOOGLE_CLIENT_ID: str | None = None

    JWT_SECRET: str = "dev-secret-change-me"
    JWT_ALG: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings() 