import logging

from fastapi import FastAPI

from .healthcheck import healthcheck_setup

logger = logging.getLogger(__name__)


def setup_routes(app: FastAPI):

    healthcheck_router = healthcheck_setup()
    app.include_router(router=healthcheck_router)

    logger.info("Routes set up successfully!")
