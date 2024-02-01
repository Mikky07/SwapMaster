import logging

from fastapi import FastAPI

from .healthcheck import setup_healthcheck
from .currency import setup_currency
from .method import setup_method

logger = logging.getLogger(__name__)


def setup_routes(app: FastAPI):

    healthcheck_router = setup_healthcheck()
    app.include_router(router=healthcheck_router)

    currency_router = setup_currency()
    app.include_router(currency_router)

    method_router = setup_method()
    app.include_router(method_router)

    logger.info("Routers set up successfully!")
