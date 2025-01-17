"""Utils module."""

import sys
import winreg
import datetime

from contextlib import suppress

from duckdb import DuckDBPyConnection
from loguru import logger

from enums import ProxyStatus
from settings import get_settings

settings = get_settings()

RULES_PK_SEQUENCE = 'rules_id_seq'


class RuntimeMark:
    """Class for store runtime mark with last updated timestamp."""

    time_mark = int(datetime.datetime.now().timestamp())  # noqa: DTZ005


def set_proxy_settings_as(proxy_status: ProxyStatus) -> None:
    """Change proxy settings in windows registry.

    :param proxy_status: enable or disable proxy settings.
    """
    key_path = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(
                key,
                'AutoConfigURL',
                0,
                winreg.REG_SZ,
                f'http://localhost:{settings.PORT}/get_pac?mark={RuntimeMark.time_mark}',
            )
            winreg.SetValueEx(key, 'AutoConfigProxy', 0, winreg.REG_DWORD, proxy_status)
    except FileNotFoundError:
        logger.error('AutoConfigURL registry key not found.')
        raise
    except Exception:  # noqa: BLE001
        logger.exception('Unexpected error while change proxy status.')
    else:
        logger.debug('Proxy {status}', status='enabled' if proxy_status else 'disabled')


def set_auto_startup(*, enable_auto_startup: bool) -> None:
    """Set auto startup for PyPac server."""
    key_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
    value_name = 'PyPac server'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            if enable_auto_startup:
                winreg.SetValueEx(
                    key,
                    value_name,
                    0,
                    winreg.REG_SZ,
                    sys.executable,
                )
            else:
                with suppress(FileNotFoundError):
                    winreg.DeleteValue(key, value_name)
    except FileNotFoundError:
        logger.error('AutoStartup registry key not found.')
        raise
    except Exception:  # noqa: BLE001
        logger.exception('Unexpected error while set auto startup status.')
    else:
        logger.debug('Auto startup {status}', status='enabled' if enable_auto_startup else 'disabled')

def init_db(db: DuckDBPyConnection) -> None:
    """Initialize database.

    :param db: database connection
    """
    db.sql(
        'CREATE TABLE IF NOT EXISTS rules '
        '( id INTEGER NOT NULL PRIMARY KEY, rule VARCHAR, is_active BOOLEAN NOT NULL);',
    )
    db.sql(
        f'CREATE SEQUENCE IF NOT EXISTS {RULES_PK_SEQUENCE} START 1 INCREMENT 1;',
    )
