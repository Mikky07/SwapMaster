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
    MethodGateway,
)
from swapmaster.application import (
    Authenticate,
    AddRequisite,
    AddOrder,
    FinishOrder,
    CancelOrder,
    CalculateSendTotal,
    AddPair,
    AddMethod,
    CreateCommission,
    GetFullOrder,
)
from swapmaster.application.common import Notifier
from swapmaster.application.common.task_manager import TaskManager
from swapmaster.application.order import SetOrderPaidUp
from swapmaster.application.verifier import Verifier, UserVerificationCash
from swapmaster.common.config.models import Config
from swapmaster.core.services import (
    UserService,
    RequisiteService,
    OrderService,
    PairService,
    MethodService,
    CommissionService,
)
from swapmaster.presentation.interactor_factory import InteractorFactory
from swapmaster.main.db_uow import UowAsyncSession
from swapmaster.main.providers import new_order_gateway


class IoC(InteractorFactory):
    def __init__(
        self,
        task_manager: TaskManager,
        notifier: Notifier,
        config: Config,
        db_connection_pool: async_sessionmaker[AsyncSession],
        user_verification_cash: UserVerificationCash,
    ):
        self.task_manager = task_manager
        self.config = config
        self.db_connection_pool = db_connection_pool
        self.user_verification_cash = user_verification_cash
        self.user_service = UserService()
        self.requisite_service = RequisiteService()
        self.order_service = OrderService()
        self.pair_service = PairService()
        self.method_service = MethodService()
        self.commission_service = CommissionService()
        self.notifier = notifier

    @asynccontextmanager
    async def get_verifier(self) -> Verifier:
        async with self.db_connection_pool() as session:
            yield Verifier(
                uow=UowAsyncSession(session=session),
                notifier=self.notifier,
                cash=self.user_verification_cash,
            )

    @asynccontextmanager
    async def get_authenticator(self) -> Authenticate:
        async with self.db_connection_pool() as session:
            uow_async_session = UowAsyncSession(session=session)
            verifier = Verifier(
                uow=uow_async_session,
                notifier=self.notifier,
                cash=self.user_verification_cash,
            )
            user_saver = UserGateway(session)
            yield Authenticate(
                user_saver=user_saver,
                uow=uow_async_session,
                user_service=self.user_service,
                verifier=verifier,
            )

    @asynccontextmanager
    async def requisite_creator(self) -> AddRequisite:
        async with self.db_connection_pool() as session:
            yield AddRequisite(
                requisite_gateway=RequisiteGateway(session),
                uow=UowAsyncSession(session),
                requisite_service=self.requisite_service,
            )

    @asynccontextmanager
    async def order_creator(self) -> AddOrder:
        async with self.db_connection_pool() as session:
            yield AddOrder(
                order_service=self.order_service,
                pair_gateway=PairGateway(session),
                requisites_gateway=RequisiteGateway(session),
                order_requisite_gateway=OrderRequisiteGateway(session),
                reserve_gateway=ReserveGateway(session),
                notifier=self.notifier,
                task_manager=self.task_manager,
                config=self.config.central,
                order_gateway=OrderGateway(session),
                user_reader=UserGateway(session),
                uow=UowAsyncSession(session),
                order_gateway_factory=new_order_gateway(self.db_connection_pool),
            )

    @asynccontextmanager
    async def order_finisher(self) -> FinishOrder:
        async with self.db_connection_pool() as session:
            yield FinishOrder(
                uow=UowAsyncSession(session),
                reserve_gateway=ReserveGateway(session),
                pair_reader=PairGateway(session),
                user_reader=UserGateway(session),
                notifier=self.notifier,
                order_gateway=OrderGateway(session),
            )

    @asynccontextmanager
    async def order_canceler(self) -> CancelOrder:
        async with self.db_connection_pool() as session:
            yield CancelOrder(
                uow=UowAsyncSession(session),
                order_updater=OrderGateway(session),
                user_reader=UserGateway(session),
                notifier=self.notifier,
            )

    @asynccontextmanager
    async def send_total_calculator(self) -> CalculateSendTotal:
        async with self.db_connection_pool() as session:
            yield CalculateSendTotal(
                commission_gateway=CommissionGateway(session),
                pair_gateway=PairGateway(session),
            )

    @asynccontextmanager
    async def pair_creator(self) -> AddPair:
        async with self.db_connection_pool() as session:
            yield AddPair(
                pair_gateway=PairGateway(session),
                pair_service=self.pair_service,
                uow=UowAsyncSession(session),
            )

    @asynccontextmanager
    async def method_creator(self) -> AsyncContextManager[AddMethod]:
        async with self.db_connection_pool() as session:
            yield AddMethod(
                method_db_gateway=MethodGateway(session),
                method_service=self.method_service,
                uow=UowAsyncSession(session),
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
    async def full_order_fetcher(self) -> GetFullOrder: ...

    @asynccontextmanager
    async def set_order_as_paid(self) -> AsyncContextManager[SetOrderPaidUp]:
        async with self.db_connection_pool() as session:
            yield SetOrderPaidUp(
                uow=UowAsyncSession(session=session),
                order_gateway=OrderGateway(session=session),
                task_manager=self.task_manager,
            )
