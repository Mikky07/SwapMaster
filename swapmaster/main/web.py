import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from swapmaster.common.config.models import Paths
from swapmaster.common.config.parser import get_paths
from swapmaster.common.config.parser import logging_setup
from swapmaster.presentation.api import *
from swapmaster.presentation.api.routes import setup_routers
from swapmaster.main.di import setup_dependencies


def setup() -> FastAPI:
    paths = get_paths_common()

    api_config = load_api_config(paths=paths)
    logging_setup(paths=paths)

    # this instance will be used by all app
    scheduler = AsyncIOScheduler()
    scheduler.start()

    app = FastAPI()

    setup_routers(app)

    setup_dependencies(
        app=app,
        api_config=api_config,
        scheduler=scheduler
    )

    return app


def get_paths_common() -> Paths:
    return get_paths("API_PATH")


if __name__ == "__main__":
    uvicorn.run(setup(), host="127.0.0.1", port=8000)
