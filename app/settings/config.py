from pydantic import BaseSettings


class Settings(BaseSettings):
    """Config of microservice"""
    VERSION: str = '1.0'
    LOG_LEVEL: str = 'INFO'
    SERVICE_NAME: str = 'OSAI TEST'
    SERVICE_PORT: int = 80

    # sentry config
    ENABLE_SENTRY: bool = False
    SENTRY_DSN: str = ''

    # Postgres settings
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'osai_test'
    POSTGRES_PORT: str = 5432

    class Config:
        case_sensitive = True
        env_file = '.env'


config = Settings()
