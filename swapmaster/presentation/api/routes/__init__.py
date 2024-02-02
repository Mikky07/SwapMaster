import logging

from fastapi import FastAPI

from .healthcheck import setup_healthcheck
from .currency import setup_currency
from .method import setup_method
from .commission import setup_commission

logger = logging.getLogger(__name__)


def setup_routes(app: FastAPI):

    routers = (
        setup_commission(),
        setup_currency(),
        setup_healthcheck(),
        setup_method()
    )

    for router in routers:
        app.include_router(router)

    logger.info("Routers set up successfully!")
