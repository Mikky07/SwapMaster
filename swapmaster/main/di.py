import logging
from typing import TypeVar

from adaptix import Retort
from aiogram import Dispatcher
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from dishka.integrations.aiogram import setup_dishka as setup_dishka_aiogram
from fastapi import FastAPI
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from swapmaster.adapters.db.factory import create_pool, create_redis
from swapmaster.adapters.db.gateways.redis import VerificationCashImp
from swapmaster.adapters.mq.notification.config import EmailConfig
from swapmaster.application.common.verifier import VerificationCash
from swapmaster.common.config.models.central import CentralConfig
from swapmaster.presentation.tgbot.config.models.main import BotConfig
from swapmaster.presentation.tgbot.middlewares import setup_middlewares
from swapmaster.presentation.tgbot.providers import TGUserProvider, TGBotNotifierProvider, TGBotVerifierProvider
from swapmaster.presentation.web_api.config.models.main import APIConfig
from swapmaster.main.ioc import (
    InteractorProvider,
    GatewayProvider,
    WebInteractorProvider,
    ServiceProvider,
    TaskManagerProvider,
    RedisVerificationCashProvider,
    EmailNotifierProvider
)
from swapmaster.presentation.web_api.providers.auth import AuthProvider


logger = logging.getLogger(__name__)


T = TypeVar("T")


def singleton(value: T):
    def get_value() -> T:
        return value

    return get_value


def setup_bot_di(
    dp: Dispatcher,
    bot_config: BotConfig,
):
    pool = create_pool(bot_config.db)

    redis = create_redis(bot_config.redis)
    user_verification_cash = VerificationCashImp(redis=redis)

    retort = Retort()

    container = make_async_container(
        InteractorProvider(),
        GatewayProvider(),
        ServiceProvider(),
        TaskManagerProvider(),
        TGUserProvider(),
        TGBotNotifierProvider(),
        TGBotVerifierProvider(),
        context={
            CentralConfig: bot_config.central,
            VerificationCash: user_verification_cash,
            async_sessionmaker[AsyncSession]: pool,
            Retort: retort
        }
    )

    setup_middlewares(dp=dp)
    setup_dishka_aiogram(container=container, router=dp, auto_inject=True)


def setup_web_di(
    app: FastAPI,
    api_config: APIConfig,
):
    pool = create_pool(api_config.db)

    redis = create_redis(api_config.redis)
    user_verification_cash = VerificationCashImp(redis=redis)

    container = make_async_container(
        InteractorProvider(),
        GatewayProvider(),
        WebInteractorProvider(),
        ServiceProvider(),
        TaskManagerProvider(),
        RedisVerificationCashProvider(),
        AuthProvider(),
        EmailNotifierProvider(),
        context={
            CentralConfig: api_config.central,
            VerificationCash: user_verification_cash,
            async_sessionmaker[AsyncSession]: pool,
            Redis: redis,
            logging.Logger: logger,
            EmailConfig: api_config.email
        }
    )

    setup_dishka_fastapi(container=container, app=app)
