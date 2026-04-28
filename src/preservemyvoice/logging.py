import logging
import sys
from logging.config import dictConfig

from .config import settings


def setup_logging() -> None:
    """Configure structured logging."""
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "default",
                },
            },
            "loggers": {
                "": {"level": log_level, "handlers": ["console"]},
                "uvicorn": {"level": "WARNING", "handlers": ["console"]},
                "uvicorn.access": {"level": "WARNING", "handlers": ["console"]},
            },
        }
    )


logger = logging.getLogger(__name__)
