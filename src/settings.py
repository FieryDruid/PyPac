"""Settings module."""
import sys

from pathlib import Path
from functools import lru_cache

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

from enums import LogLevel
from data.pac_text import PAC_TEXT
from data.env_settings import DEFAULT_SETTINGS

is_bundled = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

def get_data_file_path(file_name: str, *, is_bundled: bool) -> Path:
    """Get path to data file."""
    return Path(sys.executable).parent / file_name if is_bundled else Path(__file__).parent.parent / file_name

_ENV_FILE_PATH = get_data_file_path('settings.env', is_bundled=is_bundled)
_PAC_FILE_PATH = get_data_file_path('pac.txt', is_bundled=is_bundled)

def _create_file(file_path: Path, content: str) -> None:
    """Create file with given content.

    :param file_path: path to file
    :param content: content for file
    """
    with file_path.open('w', encoding='utf-8') as file:
        file.write(content)

if is_bundled:
    if not _ENV_FILE_PATH.exists():
        logger.debug('Create settings file with defaults.')
        _create_file(_ENV_FILE_PATH, DEFAULT_SETTINGS)
    if not _PAC_FILE_PATH.exists():
        logger.debug('Create PAC file.')
        _create_file(_PAC_FILE_PATH, PAC_TEXT)


with _PAC_FILE_PATH.open('r', encoding='utf-8') as file:
    _pac_content = file.read()


class Settings(BaseSettings):
    """Project settings."""

    model_config = SettingsConfigDict(env_file=_ENV_FILE_PATH, env_file_encoding='utf-8')

    PROXY_DOMAIN: str = '127.0.0.1'
    PROXY_PORT: int = '12334'

    LOG_LEVEL: LogLevel = LogLevel.DEBUG
    PORT: int = 8081
    AUTO_STARTUP: bool = False

    @property
    def PAC_TEXT(self) -> Path:  # noqa: N802
        """Return path to pac.txt."""
        return _pac_content

    @property
    def IS_BUNDLED(self) -> bool:  # noqa: N802
        """Application bundled status."""
        return is_bundled

@lru_cache(1)
def get_settings() -> Settings:
    """Get project settings."""
    return Settings()
