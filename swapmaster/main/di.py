import logging
from typing import TypeVar

from apscheduler import Scheduler, AsyncScheduler
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from swapmaster.adapters.db.factory import create_pool, create_redis
from swapmaster.adapters.db.gateways.redis import UserVerificationCashImp
from swapmaster.adapters.db.gateways.sqlalchemy import *
from swapmaster.application.common.db import *
from swapmaster.core.models import User
from swapmaster.main.ioc import IoC
from swapmaster.presentation.api.config.models.main import APIConfig
from swapmaster.presentation.interactor_factory import InteractorFactory
from swapmaster.presentation.api.depends.auth import AuthProvider
from swapmaster.main.providers import DBGatewayProvider, async_session_provider


logger = logging.getLogger(__name__)


T = TypeVar("T")


def singleton(value: T):
    def get_value() -> T:
        return value

    return get_value


def setup_dependencies(
    app: FastAPI,
    api_config: APIConfig,
    scheduler_sync: Scheduler,
    scheduler_async: AsyncScheduler,
):
    pool = create_pool(api_config.db)

    redis = create_redis(api_config.redis)
    user_verification_cash = UserVerificationCashImp(redis=redis)

    ioc = IoC(
        scheduler_async=scheduler_async,
        scheduler_sync=scheduler_sync,
        api_config=api_config,
        db_connection_pool=pool,
        user_verification_cash=user_verification_cash,
        central_config=api_config.central,
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
            MethodListReader: DBGatewayProvider(MethodGateway),
            OrderReader | OrderUpdater: DBGatewayProvider(OrderGateway),
            PairReader: DBGatewayProvider(PairGateway),
            OrderRequisiteReader: DBGatewayProvider(OrderRequisiteGateway),
            UserReader: DBGatewayProvider(UserReader),
            User: auth_provider.get_current_user,
        }
    )

    logger.info("dependencies set up!")
