"""Get rules dependencies."""
from typing import Annotated, TypeAlias
from collections.abc import Generator

from fastapi import Depends

from dependencies.db import DbConnect


def get_user_rules(db: DbConnect) -> Generator[str, None, None]:
    """Get all active user rules.

    :param db: Database connection.
    :yield: active proxy rule string from database.
    """
    for item in db.sql('SELECT rule FROM rules WHERE is_active = True;').fetchall():
        yield item[0]


UserRules: TypeAlias = Annotated[Generator[str], Depends(get_user_rules)]
