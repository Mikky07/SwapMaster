import asyncio
import uvicorn

from fastapi import FastAPI

from swapmaster.common.config.models import Paths
from swapmaster.common.config.parser import get_paths
from swapmaster.common.config.parser import logging_setup
from swapmaster.presentation.api import *
from swapmaster.presentation.api.routes import setup_routers
from swapmaster.main.di import setup_dependencies
from swapmaster.adapters.mq import create_async_scheduler, create_sync_scheduler


def setup() -> FastAPI:
    paths = get_paths_common()

    api_config = load_api_config(paths=paths)
    logging_setup(paths=paths)

    app = FastAPI()
    setup_routers(app)

    scheduler_async = asyncio.run(create_async_scheduler())
    scheduler_sync = create_sync_scheduler()

    setup_dependencies(
        app=app,
        api_config=api_config,
        scheduler_async=scheduler_async,
        scheduler_sync=scheduler_sync
    )

    return app


def get_paths_common() -> Paths:
    return get_paths("API_PATH")


if __name__ == "__main__":
    uvicorn.run(setup(), host="127.0.0.1", port=8000)
