"""Pac script generator."""
from collections.abc import Iterable, Generator

from settings import get_settings

settings = get_settings()


PROXY_ADDRESS = f"var __PROXY__ = 'PROXY {settings.PROXY_DOMAIN}:{settings.PROXY_PORT};';"
START_USERRULES = 'var __USERRULES__ = ['
END_USERRULES = '];'


def gen_pac_content(user_rules: Iterable[str]) -> Generator[str, None, None]:
    """Generate pac script content by user rules.

    :param user_rules: Iterable object with string user rules.
    :yield: pac script text content
    """
    yield f'{PROXY_ADDRESS}\n'
    yield f'{START_USERRULES}\n'
    for user_rule in user_rules:
        yield f'  "{user_rule}",\n'
    yield f'{END_USERRULES}\n'
    yield settings.PAC_TEXT
