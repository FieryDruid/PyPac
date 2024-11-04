"""Pac script generator."""

from pathlib import Path
from collections.abc import Iterable, Generator

START_USERRULES = 'var __USERRULES__ = ['
END_USERRULES = '];'

base_pac_path = Path().cwd() / 'src' / 'pac' / 'pac.txt'

with base_pac_path.open('r', encoding='utf-8') as file:
    main_pac_content = file.read()


def gen_pac_content(user_rules: Iterable[str]) -> Generator[str, None, None]:
    """Generate pac script content by user rules.

    :param user_rules: Iterable object with string user rules.
    :yield: pac script text content
    """
    yield f'{START_USERRULES}\n'
    for user_rule in user_rules:
        yield f'  "{user_rule}",\n'
    yield f'{END_USERRULES}\n'
    yield main_pac_content
