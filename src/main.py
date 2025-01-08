"""Main module with base app."""

import sys

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

import uvicorn

from loguru import logger
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from enums import ProxyStatus
from utils import init_db, set_auto_startup, set_proxy_settings_as
from settings import get_settings
from routes.pac import router as pac_router
from database.connection import get_connection

settings = get_settings()

def init_logger() -> None:
    """Initialize logger."""
    logger.remove()
    logger.add(sys.stdout, level=settings.LOG_LEVEL)



@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """FastAPI lifespan function.

    :param app: FastAPI instance
    """
    init_logger()
    set_proxy_settings_as(ProxyStatus.ENABLED)
    if settings.IS_BUNDLED:
        set_auto_startup(enable_auto_startup=settings.AUTO_STARTUP)

    db = get_connection()
    init_db(db)

    yield

    db.close()
    set_proxy_settings_as(ProxyStatus.DISABLED)


app = FastAPI(
    docs_url='/docs',
    lifespan=lifespan,
    title='PyPac swagger.',
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(pac_router, tags=['PAC-script'])


if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=settings.PORT,
        reload=False,
        log_level=settings.LOG_LEVEL.lower(),
    )
