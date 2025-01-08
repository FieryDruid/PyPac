"""Provides a singleton connection to a database."""
from functools import lru_cache

import duckdb

from settings import get_settings, get_data_file_path

settings = get_settings()

current_path = get_data_file_path('data.duckdb', is_bundled=settings.IS_BUNDLED)

@lru_cache(1)
def get_connection() -> duckdb.DuckDBPyConnection:
    """Get database connection.

    :return: Database connection.
    """
    return duckdb.connect(current_path)

