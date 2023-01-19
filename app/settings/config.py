from pydantic import BaseSettings


class Settings(BaseSettings):
    """Microservice config"""
    VERSION: str = '1.0'
    LOG_LEVEL: str = 'INFO'
    SERVICE_NAME: str = 'OSAI TEST'
    SERVICE_PORT: int = 80

    MAX_KEY_LENGTH: int = 8  # up to 36 but then easier to use uuid4 as hash func

    # Postgres settings
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'osai_test'
    POSTGRES_PORT: int = 5432
    MIN_POOL_SIZE: int = 1
    MAX_POOL_SIZE: int = 5

    class Config:
        case_sensitive = True
        env_file = '.env'


config = Settings()
