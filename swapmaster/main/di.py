import logging
from typing import TypeVar

from aiogram import Dispatcher
from apscheduler import Scheduler, AsyncScheduler
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from swapmaster.adapters.db.factory import create_pool, create_redis
from swapmaster.adapters.db.gateways.redis import VerificationCashImp
from swapmaster.adapters.db.gateways.sqlalchemy import *
from swapmaster.adapters.mq.notification import EmailNotifier
from swapmaster.adapters.mq.notification.bot_notifier import TGBotNotifier
from swapmaster.adapters.mq.scheduler import SyncTaskManager, AsyncTaskManagerImpl
from swapmaster.application.common.gateways import OrderRequisiteReader, UserReader, PairReader, OrderReader, \
    OrderUpdater, MethodReader, RequisiteReader, CurrencyListReader
from swapmaster.core.models import User
from swapmaster.main.ioc import IoC
from swapmaster.presentation.tgbot.config.models.main import BotConfig
from swapmaster.presentation.web_api.config.models.main import APIConfig
from swapmaster.presentation.interactor_factory import InteractorFactory
from swapmaster.presentation.web_api.depends.auth import AuthProvider
from swapmaster.presentation.tgbot.middlewares.setup import setup_middlewares
from swapmaster.main.providers import DBGatewayProvider, async_session_provider


logger = logging.getLogger(__name__)


T = TypeVar("T")


def singleton(value: T):
    def get_value() -> T:
        return value

    return get_value


def setup_bot_dependencies(
    dp: Dispatcher,
    bot_config: BotConfig,
    scheduler_sync: Scheduler,
    scheduler_async: AsyncScheduler,
):
    pool = create_pool(bot_config.db)

    redis = create_redis(bot_config.redis)
    user_verification_cash = VerificationCashImp(redis=redis)

    sync_task_manager = SyncTaskManager(scheduler=scheduler_sync)
    async_task_manager = AsyncTaskManagerImpl(scheduler=scheduler_async)
    notifier = TGBotNotifier()

    ioc = IoC(
        config=bot_config,
        db_connection_pool=pool,
        user_verification_cash=user_verification_cash,
        notifier=notifier,
        sync_task_manager=sync_task_manager,
        async_task_manager=async_task_manager
    )

    setup_middlewares(dp=dp, ioc=ioc)


def setup_web_dependencies(
    app: FastAPI,
    api_config: APIConfig,
    scheduler_sync: Scheduler,
    scheduler_async: AsyncScheduler,
):
    pool = create_pool(api_config.db)

    redis = create_redis(api_config.redis)
    user_verification_cash = VerificationCashImp(redis=redis)

    sync_task_manager = SyncTaskManager(scheduler=scheduler_sync)
    async_task_manager = AsyncTaskManagerImpl(scheduler=scheduler_async)
    notifier = EmailNotifier(config=api_config.email, task_manager=sync_task_manager)

    ioc = IoC(
        config=api_config,
        db_connection_pool=pool,
        user_verification_cash=user_verification_cash,
        notifier=notifier,
        async_task_manager=async_task_manager,
        sync_task_manager=sync_task_manager
    )

    auth_provider = AuthProvider(config=api_config.auth)

    app.dependency_overrides.update(
        {
            InteractorFactory: singleton(ioc),
            AuthProvider: lambda: auth_provider,
            AsyncSession: async_session_provider(pool),
            CurrencyListReader: DBGatewayProvider(CurrencyGateway),
            RequisiteReader: DBGatewayProvider(RequisiteGateway),
            OrderRequisiteGateway: DBGatewayProvider(OrderRequisiteGateway),
            MethodReader: DBGatewayProvider(MethodGateway),
            OrderReader | OrderUpdater: DBGatewayProvider(OrderGateway),
            PairReader: DBGatewayProvider(PairGateway),
            OrderRequisiteReader: DBGatewayProvider(OrderRequisiteGateway),
            UserReader: DBGatewayProvider(UserReader),
            User: auth_provider.get_current_user,
        }
    )

    logger.info("dependencies set up!")
