import asyncio
from typing import AsyncContextManager

import uvicorn
from apscheduler import AsyncScheduler
from fastapi import FastAPI

from swapmaster.common.config.models import Paths
from swapmaster.common.config.parser import get_paths
from swapmaster.common.config.parser import logging_setup
from swapmaster.presentation.api import *
from swapmaster.presentation.api.routes import setup_routers
from swapmaster.main.di import setup_dependencies
from swapmaster.adapters.mq import (
    create_async_scheduler,
    create_sync_scheduler,
    async_scheduler_startup_handler
)


def get_lifespan(scheduler_async: AsyncScheduler):
    async def lifespan(_) -> AsyncContextManager[None]:
        async with async_scheduler_startup_handler(scheduler=scheduler_async):
            yield

    return lifespan


def setup() -> FastAPI:
    paths = get_paths_common()

    api_config = load_api_config(paths=paths)
    logging_setup(paths=paths)

    scheduler_async = create_async_scheduler()
    scheduler_sync = create_sync_scheduler()

    app = FastAPI(lifespan=get_lifespan(scheduler_async=scheduler_async))
    setup_routers(app)

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
