from enum import Enum


class HttpErrorEnum(str, Enum):
    """Str enumerate for http errors"""
    URL_CREATED_409 = 'Url already created'
    BAD_KEY_GENERATION_400 = "Can't create url due collision"
    CREATION_ERROR_400 = "Can't create record"
    URL_NOT_FOUND_404 = 'No url found'
    NO_DB_POOL_503 = "Database pool connection opener error"
    BAD_URL_422 = 'Bad url'
