import functools
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Настройки проекта и окружений
    """

    # Project
    PROJECT_NAME: str = "Krestovsky"
    PROJECT_VERSION: str = "1.0.0"
    DESCRIPTION: str = "Webtronics test task"
    DEBUG: bool = True

    # DB
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    DATABASE_URL = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = os.getenv("REDIS_PORT", 6379)

    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    REFRESH_SECRET_KEY: str = os.getenv("REFRESH_SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Hunter.io
    HUNTER_API_KEY: str = os.getenv("HUNTER_API_KEY")
    HUNTER_API_URL: str = "https://api.hunter.io/v2/"
    HUNTER_VERIFY_ENDPOINT: str = "email-verifier"
    HUNTER_SUCCESS_STATUSES: tuple = ("valid", "accept_all", "webmail", "disposable")


@functools.lru_cache()
def _build_settings() -> Settings:
    return Settings()


settings = _build_settings()
