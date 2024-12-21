"""Rules repository."""
from typing import Self
from threading import Lock

from loguru import logger

from database.connection import get_connection


class RulesRepository:
    """Singleton rules repository."""

    _instance = None
    _instance_lock = Lock()

    def __new__(cls) -> Self:
        """Create singleton rules repository.

        :return: RulesRepository instance
        """
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        """Initialize rules repository."""
        with self._instance_lock:
            if getattr(self, '_initialized', None):
                return

            logger.debug('Init rules repository.')
            self._rules_lock = Lock()
            self._rules = []
            self._cache_is_valid = False
            self._db = get_connection()
            self._initialized = True

    def get_rules(self) -> list[str]:
        """Get list of rules.

        :return: Rules list.
        """
        with self._rules_lock:
            if not self._cache_is_valid:
                self._refresh_cache()
            return self._rules

    def invalidate(self) -> None:
        """Invalidate rules cache."""
        with self._rules_lock:
            self._cache_is_valid = False

    def _refresh_cache(self) -> None:
        """Refresh rules cache from database."""
        logger.debug('Set new rules from db.')
        self._rules = [
            item[0] for item in self._db.sql('SELECT rule FROM rules WHERE is_active = True;').fetchall()
        ]
        self._cache_is_valid = True
