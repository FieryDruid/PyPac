"""Provides a singleton connection to a database."""
from pathlib import Path
from functools import lru_cache

import duckdb

current_path = Path.cwd() / 'data.duckdb'

@lru_cache(1)
def get_connection() -> duckdb.DuckDBPyConnection:
    """Get database connection.

    :return: Database connection.
    """
    return duckdb.connect(current_path)

