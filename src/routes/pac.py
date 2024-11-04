"""Pac script routes."""

import datetime

from loguru import logger
from fastapi import Request, APIRouter
from fastapi.responses import StreamingResponse

from enums import ProxyStatus
from utils import RULES_PK_SEQUENCE, RuntimeMark, set_proxy_settings_as
from pac.generator import gen_pac_content
from dependencies.db import DbConnect
from dependencies.get_rules import UserRules

router = APIRouter()


@router.post('/set_rule', status_code=200, description='Add new rule.')
def set_rule(db: DbConnect, rule: str) -> int:
    """Add new rule.

    :param db: database connection.
    :param rule: rule string.
    :return: rule id.
    """
    query = f"INSERT INTO rules (id, rule, is_active) VALUES (nextval('{RULES_PK_SEQUENCE}'), ?, ?) RETURNING id"  # noqa: S608
    result = db.execute(query, [rule, True])
    rule_id: int = result.fetchone()[0]
    reset_proxy_settings()
    return rule_id


@router.delete('/remove_rule', status_code=204)
def remove_rule(db: DbConnect, rule: str) -> None:
    """Delete rule from pac script.

    :param db: Database connection.
    :param rule: Rule string.
    """
    db.execute('DELETE FROM rules WHERE rule = ?', [rule])
    reset_proxy_settings()


@router.get('/get_pac', description='Get PAC-script.')
def get_pac(user_rules: UserRules, mark: int, request: Request) -> StreamingResponse:
    """Get PAC-script.

    :param user_rules: Generator with active rules from db.
    :param mark: timestamp with time mark.
    :param request: Request object.
    :return: PAC-script file.
    """
    if mark != RuntimeMark.time_mark:
        logger.debug('Accept request with outdated time mark {headers}', headers=request.headers)
    return StreamingResponse(
        gen_pac_content(user_rules),
        status_code=200,
        headers={'Content-type': 'text/plain; charset=utf-8'},
    )


@router.get('/reset_proxy', status_code=204)
def reset_proxy_settings():
    """Reset windows proxy settings."""
    logger.info('Running proxy settings update.')
    RuntimeMark.time_mark = int(datetime.datetime.now().timestamp())  # noqa: DTZ005
    for proxy_status in (ProxyStatus.DISABLED, ProxyStatus.ENABLED):
        set_proxy_settings_as(proxy_status)
    logger.info('Proxy settings update successfully!')
