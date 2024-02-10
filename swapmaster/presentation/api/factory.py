from fastapi import FastAPI

from swapmaster.common.config.models import Paths
from .config.models.main import APIConfig
from .routes import *
from .depends import *
from swapmaster.adapters.db.factory import create_pool
from swapmaster.common.config.parser import (
    get_paths,
)


def create_app(api_config: APIConfig):
    app = FastAPI()
    pool = create_pool(api_config.db)

    setup_dependencies(
        app=app,
        pool=pool,
        config=api_config
    )
    setup_routers(app)

    return app


def get_paths_common() -> Paths:
    return get_paths("API_PATH")
