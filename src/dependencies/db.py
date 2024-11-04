"""Database module."""
from typing import Annotated, TypeAlias

from duckdb import DuckDBPyConnection
from fastapi import Depends

from database.connection import get_connection

__all__ = ['DbConnect']

DbConnect: TypeAlias = Annotated[DuckDBPyConnection, Depends(get_connection)]
