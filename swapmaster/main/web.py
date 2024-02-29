import uvicorn
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from swapmaster.common.config.models import Paths
from swapmaster.common.config.parser import get_paths
from swapmaster.common.config.parser import logging_setup
from swapmaster.presentation.api import *


def singleton(class_):
    instances = {}

    def instance_of_class(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return instance_of_class


def setup() -> FastAPI:
    paths = get_paths_common()

    api_config = load_api_config(paths=paths)
    logging_setup(paths=paths)

    scheduler = singleton(BackgroundScheduler)()
    scheduler.start()

    app = create_app(
        api_config=api_config,
        scheduler=scheduler
    )

    return app


def get_paths_common() -> Paths:
    return get_paths("API_PATH")


if __name__ == "__main__":
    uvicorn.run(setup(), host="127.0.0.1", port=8000)
