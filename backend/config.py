from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Base
    APP_NAME: str = "Pronote 2.0"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Base de données
    DATABASE_URL: str = "postgresql+asyncpg://pronote:pronote@localhost:5432/pronote_db"

    # Sécurité JWT
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 heures

    class Config:
        env_file = ".env"


settings = Settings()
