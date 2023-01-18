import logging
from logging.config import dictConfig

from app.settings.config import config

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": f'[%(asctime)s %(levelprefix)s /{config.SERVICE_NAME} %(pathname)s %(funcName)s] - %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": f'[%(asctime)s %(levelprefix)s /{config.SERVICE_NAME}] '
                   f'- "%(request_line)s" %(status_code)s',
            "use_colors": True
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "logger": {
            "handlers": ["default"],
            "level": f"{config.LOG_LEVEL}"
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": f"{config.LOG_LEVEL}",
            "propagate": False
        },
    },
}

dictConfig(log_config)  # Setting for logging
logger = logging.getLogger('logger')
