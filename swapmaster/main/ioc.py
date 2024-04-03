from contextlib import asynccontextmanager
from typing import AsyncContextManager, Iterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from swapmaster.adapters.db.gateways.sqlalchemy import (
    UserGateway,
    RequisiteGateway,
    OrderGateway,
    PairGateway,
    OrderRequisiteGateway,
    ReserveGateway,
    CommissionGateway,
    MethodGateway, CourseGateway,
)
from swapmaster.application import (
    CreateUser,
    CreateRequisite,
    CreateOrder,
    FinishOrder,
    CancelOrder,
    CalculateSendTotal,
    CreatePair,
    CreateMethod,
    CreateCommission,
    WebVerifier
)
from swapmaster.application.common import Notifier, UoW
from swapmaster.application.common.task_manager import BaseTaskManager, AsyncTaskManager
from swapmaster.application.common.verifier import Verifier
from swapmaster.application.order import SetOrderPaidUp
from swapmaster.application.web_verifier import VerificationCash
from swapmaster.common.config.models import Config
from swapmaster.core.services import (
    UserService,
    OrderService,
    CommissionService,
)
from swapmaster.core.services.requisite import RequisiteService
from swapmaster.main.db_uow import UowAsyncSession


class TaskManagerProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_async_task_manager(self) -> AsyncTaskManager:
        ...


class NotifierProvider(Provider):
    @provide
    async def get_notifier(self) -> Notifier:
        ...


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_session(self, pool: async_sessionmaker[AsyncSession]) -> AsyncSession:
        async with pool() as session:
            yield session

    @provide
    async def get_uow(self, session: AsyncSession) -> UoW:
        yield UowAsyncSession(session)

    user_gateway = provide(UserGateway)
    pair_gateway = provide(PairGateway)
    requisite_gateway = provide(RequisiteGateway)
    order_gateway = provide(OrderGateway)
    method_gateway = provide(MethodGateway)
    reserve_gateway = provide(ReserveGateway)
    order_requisite_gateway = provide(OrderRequisiteGateway)
    commission_gateway = provide(CommissionGateway)


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    authenticator = provide(CreateUser)
    requisite_creator = provide(CreateRequisite)
    order_creator = provide(CreateOrder)
    order_finisher = provide(FinishOrder)
    order_canceler = provide(CancelOrder)
    pair_creator = provide(CreatePair)
    send_total_calculator = provide(CalculateSendTotal)
    method_creator = provide(CreateMethod)
    payer = provide(SetOrderPaidUp)
    commission_creator = provide(CreateCommission)


class WebInteractorProvider(Provider):
    web_verifier = provide(WebVerifier)

