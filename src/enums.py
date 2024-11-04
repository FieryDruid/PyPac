"""Project enums."""

from enum import Enum


class LogLevel(str, Enum):
    """Log levels."""

    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class ProxyStatus(int, Enum):
    """Proxy status enum."""

    ENABLED = 1
    DISABLED = 0
