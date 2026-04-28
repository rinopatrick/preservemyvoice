from .adapters import get_db, init_db
from .config import settings
from .domain import Base
from .logging import setup_logging

__version__ = settings.APP_VERSION
__all__ = [
    "Base",
    "get_db",
    "init_db",
    "settings",
    "setup_logging",
]
