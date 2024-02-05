import logging

from fastapi import FastAPI

from .healthcheck import setup_healthcheck
from .currency import setup_currency
from .method import setup_method
from .commission import setup_commission
from .order import setup_order
from .calculate import setup_calculator

logger = logging.getLogger(__name__)


def setup_routers(app: FastAPI):

    routers = (
        setup_commission(),
        setup_currency(),
        setup_healthcheck(),
        setup_method(),
        setup_order(),
        setup_calculator()
    )

    for router in routers:
        app.include_router(router)

    logger.info("Routers set up successfully!")
