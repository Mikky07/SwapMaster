from contextlib import asynccontextmanager
from typing import AsyncContextManager

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
from swapmaster.application.common import Notifier
from swapmaster.application.common.task_manager import BaseTaskManager, AsyncTaskManager
from swapmaster.application.order import SetOrderPaidUp
from swapmaster.application.web_verifier import VerificationCash
from swapmaster.common.config.models import Config
from swapmaster.core.services import (
    UserService,
    OrderService,
    CommissionService,
)
from swapmaster.core.services.requisite import RequisiteService
from swapmaster.presentation.interactor_factory import InteractorFactory
from swapmaster.main.db_uow import UowAsyncSession
from swapmaster.presentation.tgbot import BotInteractorFactory
from swapmaster.presentation.web_api import WebInteractorFactory


class IoC(InteractorFactory):
    def __init__(
        self,
        sync_task_manager: BaseTaskManager,
        async_task_manager: AsyncTaskManager,
        notifier: Notifier,
        config: Config,
        db_connection_pool: async_sessionmaker[AsyncSession],
        user_verification_cash: VerificationCash,
    ):
        self.sync_task_manager = sync_task_manager
        self.async_task_manager = async_task_manager
        self.config = config
        self.db_connection_pool = db_connection_pool
        self.user_verification_cash = user_verification_cash
        self.user_service = UserService()
        self.order_service = OrderService()
        self.commission_service = CommissionService()
        self.requisite_service = RequisiteService()
        self.notifier = notifier

    @asynccontextmanager
    async def get_authenticator(self) -> CreateUser:
        async with self.db_connection_pool() as session:
            uow_async_session = UowAsyncSession(session=session)
            user_gateway = UserGateway(session)
            verifier = WebVerifier(
                uow=uow_async_session,
                notifier=self.notifier,
                cash=self.user_verification_cash,
                user_gateway=user_gateway
            )
            yield CreateUser(
                user_gateway=user_gateway,
                uow=uow_async_session,
                user_service=self.user_service,
                verifier=verifier,
            )

    @asynccontextmanager
    async def requisite_creator(self) -> CreateRequisite:
        async with self.db_connection_pool() as session:
            yield CreateRequisite(
                requisite_gateway=RequisiteGateway(session),
                uow=UowAsyncSession(session),
                pair_gateway=PairGateway(session)
            )

    @asynccontextmanager
    async def order_creator(self) -> CreateOrder:
        async with self.db_connection_pool() as session:
            yield CreateOrder(
                order_service=self.order_service,
                pair_gateway=PairGateway(session),
                order_requisite_gateway=OrderRequisiteGateway(session),
                requisite_gateway=RequisiteGateway(session),
                reserve_gateway=ReserveGateway(session),
                requisite_service=self.requisite_service,
                method_gateway=MethodGateway(session),
                notifier=self.notifier,
                task_manager=self.async_task_manager,
                config=self.config.central,
                order_gateway=OrderGateway(session),
                user_gateway=UserGateway(session),
                uow=UowAsyncSession(session),
            )

    @asynccontextmanager
    async def order_finisher(self) -> FinishOrder:
        async with self.db_connection_pool() as session:
            yield FinishOrder(
                uow=UowAsyncSession(session),
                reserve_gateway=ReserveGateway(session),
                pair_gateway=PairGateway(session),
                user_gateway=UserGateway(session),
                notifier=self.notifier,
                order_gateway=OrderGateway(session),
                method_gateway=MethodGateway(session)
            )

    @asynccontextmanager
    async def order_canceler(self) -> CancelOrder:
        async with self.db_connection_pool() as session:
            yield CancelOrder(
                uow=UowAsyncSession(session),
                order_gateway=OrderGateway(session),
                user_gateway=UserGateway(session),
                notifier=self.notifier,
            )

    @asynccontextmanager
    async def send_total_calculator(self) -> CalculateSendTotal:
        async with self.db_connection_pool() as session:
            yield CalculateSendTotal(
                commission_gateway=CommissionGateway(session),
                pair_gateway=PairGateway(session),
                course_gateway=CourseGateway(session)
            )

    @asynccontextmanager
    async def pair_creator(self) -> CreatePair:
        async with self.db_connection_pool() as session:
            yield CreatePair(
                pair_gateway=PairGateway(session),
                uow=UowAsyncSession(session),
            )

    @asynccontextmanager
    async def method_creator(self) -> AsyncContextManager[CreateMethod]:
        async with self.db_connection_pool() as session:
            yield CreateMethod(
                method_gateway=MethodGateway(session),
                uow=UowAsyncSession(session)
            )

    @asynccontextmanager
    async def commission_creator(self) -> AsyncContextManager[CreateCommission]:
        async with self.db_connection_pool() as session:
            yield CreateCommission(
                commission_service=self.commission_service,
                uow=UowAsyncSession(session),
                commission_gateway=CommissionGateway(session),
            )

    @asynccontextmanager
    async def set_order_as_paid(self) -> AsyncContextManager[SetOrderPaidUp]:
        async with self.db_connection_pool() as session:
            yield SetOrderPaidUp(
                uow=UowAsyncSession(session=session),
                order_gateway=OrderGateway(session=session),
                task_manager=self.async_task_manager,
            )


class WebIoC(IoC, WebInteractorFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @asynccontextmanager
    async def get_web_verifier(self) -> WebVerifier:
        async with self.db_connection_pool() as session:
            yield WebVerifier(
                user_gateway=UserGateway(session),
                uow=UowAsyncSession(session),
                notifier=self.notifier,
                cash=self.user_verification_cash
            )


class BotIoC(IoC, BotInteractorFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
