import logging

from fastapi import FastAPI

from .healthcheck import setup_healthcheck
from .currency import setup_currency
from .method import setup_method
from .commission import setup_commission
from .order import setup_order
from .calculate import setup_calculator
from .pair import setup_pair
from .auth import setup_auth

logger = logging.getLogger(__name__)


def setup_routers(app: FastAPI):

    routers = (
        setup_commission(),
        setup_currency(),
        setup_healthcheck(),
        setup_method(),
        setup_order(),
        setup_calculator(),
        setup_pair(),
        setup_auth()
    )

    for router in routers:
        app.include_router(router)

    logger.info("Routers set up successfully!")
