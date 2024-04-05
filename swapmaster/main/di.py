import logging
from typing import TypeVar

from aiogram import Dispatcher
from apscheduler import Scheduler, AsyncScheduler
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from dishka.integrations.aiogram import setup_dishka as setup_dishka_aiogram
from fastapi import FastAPI
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from swapmaster.adapters.db.factory import create_pool, create_redis
from swapmaster.adapters.db.gateways.redis import VerificationCashImp
from swapmaster.adapters.mq.notification import EmailNotifier
from swapmaster.adapters.mq.notification.bot_notifier import TGBotNotifier
from swapmaster.adapters.mq.scheduler import SyncTaskManager
from swapmaster.application.common import Notifier
from swapmaster.application.common.verifier import VerificationCash
from swapmaster.common.config.models.central import CentralConfig
from swapmaster.presentation.tgbot.config.models.main import BotConfig
from swapmaster.presentation.web_api.config.models.main import APIConfig
from swapmaster.main.ioc import (
    InteractorProvider,
    GatewayProvider,
    WebInteractorProvider,
    ServiceProvider,
    TaskManagerProvider,
    RedisVerificationCashProvider
)
from swapmaster.presentation.tgbot.middlewares.setup import setup_middlewares


logger = logging.getLogger(__name__)


T = TypeVar("T")


def singleton(value: T):
    def get_value() -> T:
        return value

    return get_value


def setup_bot_di(
    dp: Dispatcher,
    bot_config: BotConfig,
    scheduler_sync: Scheduler,
    scheduler_async: AsyncScheduler,
):
    pool = create_pool(bot_config.db)

    redis = create_redis(bot_config.redis)
    user_verification_cash = VerificationCashImp(redis=redis)

    notifier = TGBotNotifier()

    container = make_async_container(
        InteractorProvider(),
        GatewayProvider(),
        WebInteractorProvider(),
        ServiceProvider(),
        TaskManagerProvider(),
        context={
            Scheduler: scheduler_sync,
            AsyncScheduler: scheduler_async,
            CentralConfig: bot_config.central,
            VerificationCash: user_verification_cash,
            Notifier: notifier,
            async_sessionmaker[AsyncSession]: pool,
        }
    )

    setup_dishka_aiogram(container=container, router=dp)


def setup_web_di(
    app: FastAPI,
    api_config: APIConfig,
    scheduler_sync: Scheduler,
    scheduler_async: AsyncScheduler,
):
    pool = create_pool(api_config.db)

    redis = create_redis(api_config.redis)
    user_verification_cash = VerificationCashImp(redis=redis)

    sync_task_manager = SyncTaskManager(scheduler=scheduler_sync)
    notifier = EmailNotifier(config=api_config.email, task_manager=sync_task_manager)

    container = make_async_container(
        InteractorProvider(),
        GatewayProvider(),
        WebInteractorProvider(),
        ServiceProvider(),
        TaskManagerProvider(),
        RedisVerificationCashProvider(),
        context={
            Scheduler: scheduler_sync,
            AsyncScheduler: scheduler_async,
            CentralConfig: api_config.central,
            VerificationCash: user_verification_cash,
            Notifier: notifier,
            async_sessionmaker[AsyncSession]: pool,
            Redis: redis
        }
    )

    setup_dishka_fastapi(container=container, app=app)
