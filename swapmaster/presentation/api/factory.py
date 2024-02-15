from fastapi import FastAPI

from swapmaster.presentation.api.config.models.main import APIConfig
from swapmaster.presentation.api.routes import *
from swapmaster.presentation.api.depends import *
from swapmaster.adapters.db.factory import create_pool


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
