from fastapi import FastAPI

from swapmaster.common.config.models import Paths, Config
from .routes import setup_routers
from .depends import setup_dependencies
from swapmaster.adapters.db.factory import create_pool
from swapmaster.common.config.parser import (
    get_paths,
)


def create_app(api_config: Config):
    app = FastAPI()
    pool = create_pool(api_config.db)

    setup_dependencies(app, pool)
    setup_routers(app)

    return app


def get_paths_common() -> Paths:
    return get_paths("API_PATH")
