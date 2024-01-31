import logging

from fastapi import FastAPI

from .healthcheck import setup_healthcheck
from .currency import setup_currency

logger = logging.getLogger(__name__)


def setup_routes(app: FastAPI):

    healthcheck_router = setup_healthcheck()
    app.include_router(router=healthcheck_router)

    currency_router = setup_currency()
    app.include_router(currency_router)

    logger.info("Routes set up successfully!")
