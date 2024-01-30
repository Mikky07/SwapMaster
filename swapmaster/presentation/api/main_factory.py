from fastapi import FastAPI

from swapmaster.common.config.models import Paths
from .routes import setup_routes
from swapmaster.common.config.parser import (
    get_paths,
)


def create_app():
    app = FastAPI()

    setup_routes(app)

    return app


def get_paths_common() -> Paths:
    return get_paths("API_PATH")
