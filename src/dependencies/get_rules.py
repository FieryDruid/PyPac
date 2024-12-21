"""Get rules dependencies."""

from typing import Annotated, TypeAlias
from threading import Lock

from fastapi import Depends

from database.rules_repository import RulesRepository

lock = Lock()


def get_user_rules() -> list[str]:
    """Get all active user rules.

    :param db: Database connection.
    :yield: active proxy rule string from database.
    """
    return RulesRepository().get_rules().copy()


UserRules: TypeAlias = Annotated[list[str], Depends(get_user_rules)]
