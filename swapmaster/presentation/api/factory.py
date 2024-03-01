from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from redis.asyncio import Redis

from swapmaster.presentation.api.config.models.main import APIConfig
from swapmaster.presentation.api.routes import *
from swapmaster.presentation.api.depends import *
from swapmaster.adapters.db.factory import create_pool, create_redis


def create_app(api_config: APIConfig, scheduler: BackgroundScheduler):
    app = FastAPI()
    pool = create_pool(api_config.db)

    setup_dependencies(
        app=app,
        pool=pool,
        config=api_config,
        scheduler=scheduler
    )
    setup_routers(app)

    return app
