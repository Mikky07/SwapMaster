import logging
from functools import partial

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from swapmaster.adapters.mq.notification import EmailNotifier
from swapmaster.adapters.mq.notification.config import EmailConfig
from swapmaster.application.common.db import *
from swapmaster.application import *
from swapmaster.application.common import *
from swapmaster.application.common.task_solver import TaskSolver
from swapmaster.application.verifier import Verifier, UserVerificationCash
from swapmaster.core.models import User
from swapmaster.core.services import *
from swapmaster.adapters.db.gateways.sqlalchemy import *
from swapmaster.presentation.api.config.models.auth import AuthConfig
from swapmaster.presentation.api.config.models.main import APIConfig
from swapmaster.presentation.api.depends.auth import AuthProvider
from swapmaster.presentation.api.depends.providers import (
    new_uow,
    new_db_session,
    DBGatewayProvider,
    new_verification_cash,
    new_task_solver,
    RedisProvider
)

logger = logging.getLogger(__name__)


def set_depends_as_defaults(cls: type) -> None:
    init = cls.__init__
    args_count = init.__code__.co_kwonlyargcount + init.__code__.co_argcount - 1
    init.__defaults__ = tuple(
        Depends() for _ in range(args_count)
    )
# this will be transfered to main


def setup_dependencies(
    app: FastAPI,
    pool: async_sessionmaker[AsyncSession],
    config: APIConfig,
    scheduler: BackgroundScheduler
):
    method_service = MethodService()
    commission_service = CommissionService()
    order_service = OrderService()
    pair_service = PairService()
    requisite_service = RequisiteService()
    user_service = UserService()
    redis_provider = RedisProvider(config=config.redis)
    auth_provider = AuthProvider(config=config.auth)

    app.dependency_overrides.update(
        {
            MethodWriter: DBGatewayProvider(MethodGateway),
            MethodListReader: DBGatewayProvider(MethodGateway),
            CommissionWriter: DBGatewayProvider(CommissionGateway),
            CommissionReader: DBGatewayProvider(CommissionGateway),
            UserSaver: DBGatewayProvider(UserGateway),
            OrderWriter: DBGatewayProvider(OrderGateway),
            OrderReader: DBGatewayProvider(OrderGateway),
            OrderUpdater: DBGatewayProvider(OrderGateway),
            RequisiteWriter: DBGatewayProvider(RequisiteGateway),
            RequisiteReader: DBGatewayProvider(RequisiteGateway),
            ReserveUpdater: DBGatewayProvider(ReserveGateway),
            ReserveReader: DBGatewayProvider(ReserveGateway),
            OrderRequisiteReader: DBGatewayProvider(OrderRequisiteGateway),
            OrderRequisiteWriter: DBGatewayProvider(OrderRequisiteGateway),
            CurrencyGateway: DBGatewayProvider(CurrencyGateway),
            CurrencyListReader: DBGatewayProvider(CurrencyGateway),
            PairReader: DBGatewayProvider(PairGateway),
            PairWriter: DBGatewayProvider(PairGateway),
            UserReader: DBGatewayProvider(UserGateway),
            AsyncSession: partial(new_db_session, pool),
            PairService: lambda: pair_service,
            MethodService: lambda: method_service,
            CommissionService: lambda: commission_service,
            OrderService: lambda: order_service,
            RequisiteService: lambda: requisite_service,
            UserService: lambda: user_service,
            BackgroundScheduler: lambda: scheduler,
            EmailConfig: lambda: config.email,
            AuthConfig: lambda: config.auth,
            AuthProvider: lambda: auth_provider,
            User: auth_provider.get_current_user,
            Redis: redis_provider,
            TaskSolver: new_task_solver,
            UserVerificationCash: new_verification_cash,
            Notifier: EmailNotifier,
            UoW: new_uow,
        }
    )

    set_depends_as_defaults(EmailNotifier)
    set_depends_as_defaults(AddMethod)
    set_depends_as_defaults(AddCommission)
    set_depends_as_defaults(AddOrder)
    set_depends_as_defaults(CalculateSendTotal)
    set_depends_as_defaults(AddPair)
    set_depends_as_defaults(FinishOrder)
    set_depends_as_defaults(AddRequisite)
    set_depends_as_defaults(GetFullOrder)
    set_depends_as_defaults(CancelOrder)
    set_depends_as_defaults(Authenticate)
    set_depends_as_defaults(Verifier)

    logger.info("dependencies set up!")
