from contextlib import asynccontextmanager
from typing import AsyncContextManager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from swapmaster.adapters.db.gateways.sqlalchemy import (
    UserGateway,
    RequisiteGateway,
    OrderGateway,
    PairGateway,
    OrderRequisiteGateway,
    ReserveGateway,
    CommissionGateway,
    MethodGateway
)
from swapmaster.adapters.mq.notification import EmailNotifier
from swapmaster.adapters.mq.scheduler import TaskSolverImp
from swapmaster.application import (
    Authenticate,
    AddRequisite,
    AddOrder,
    FinishOrder,
    CancelOrder,
    CalculateSendTotal,
    AddPair,
    AddMethod,
    AddCommission
)
from swapmaster.application.verifier import Verifier, UserVerificationCash
from swapmaster.common.config.models.central import CentralConfig
from swapmaster.core.services import (
    UserService,
    RequisiteService,
    OrderService,
    PairService,
    MethodService,
    CommissionService
)
from swapmaster.presentation.api.config.models.main import APIConfig
from swapmaster.presentation.interactor_factory import InteractorFactory
from swapmaster.main.db_uow import UowAsyncSession


class IoC(InteractorFactory):
    def __init__(
            self,
            scheduler: AsyncIOScheduler,
            api_config: APIConfig,
            db_connection_pool: async_sessionmaker[AsyncSession],
            user_verification_cash: UserVerificationCash,
            central_config: CentralConfig
    ):
        task_solver = TaskSolverImp(scheduler=scheduler)

        self.task_solver = task_solver
        self.central_config = central_config
        self.api_config = api_config
        self.db_connection_pool = db_connection_pool
        self.user_verification_cash = user_verification_cash
        self.user_service = UserService()
        self.requisite_service = RequisiteService()
        self.order_service = OrderService()
        self.pair_service = PairService()
        self.method_service = MethodService()
        self.commission_service = CommissionService()
        self.email_notifier = EmailNotifier(self.api_config.email, task_solver=task_solver)

    @asynccontextmanager
    async def get_verifier(self) -> Verifier:
        async with self.db_connection_pool() as session:
            yield Verifier(
                uow=UowAsyncSession(session=session),
                notifier=self.email_notifier,
                cash=self.user_verification_cash
            )

    @asynccontextmanager
    async def get_authenticator(self) -> Authenticate:
        async with self.db_connection_pool() as session:
            uow_async_session = UowAsyncSession(session=session)
            verifier = Verifier(
                uow=uow_async_session,
                notifier=self.email_notifier,
                cash=self.user_verification_cash
            )
            user_saver = UserGateway(session)
            yield Authenticate(
                user_saver=user_saver,
                uow=uow_async_session,
                user_service=self.user_service,
                verifier=verifier
            )

    @asynccontextmanager
    async def requisite_creator(self) -> AddRequisite:
        async with self.db_connection_pool() as session:
            yield AddRequisite(
                requisite_gateway=RequisiteGateway(session),
                uow=UowAsyncSession(session),
                requisite_service=self.requisite_service
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
                notifier=self.email_notifier,
                task_solver=self.task_solver,
                central_config=self.central_config,
                order_gateway=OrderGateway(session),
                user_reader=UserGateway(session),
                uow=UowAsyncSession(session),
                order_canceler=self
            )

    @asynccontextmanager
    async def order_finisher(self) -> FinishOrder:
        async with self.db_connection_pool() as session:
            yield FinishOrder(
                uow=UowAsyncSession(session),
                reserve_gateway=ReserveGateway(session),
                pair_reader=PairGateway(session),
                user_reader=UserGateway(session),
                notifier=self.email_notifier,
                order_gateway=OrderGateway(session)
            )

    @asynccontextmanager
    async def order_canceler(self) -> CancelOrder:
        async with self.db_connection_pool() as session:
            yield CancelOrder(
                uow=UowAsyncSession(session),
                order_updater=OrderGateway(session),
                user_reader=UserGateway(session),
                notifier=self.email_notifier
            )

    @asynccontextmanager
    async def send_total_calculator(self) -> CalculateSendTotal:
        async with self.db_connection_pool() as session:
            yield CalculateSendTotal(
                commission_gateway=CommissionGateway(session),
                pair_gateway=PairGateway(session)
            )

    @asynccontextmanager
    async def pair_creator(self) -> AddPair:
        async with self.db_connection_pool() as session:
            yield AddPair(
                pair_gateway=PairGateway(session),
                pair_service=self.pair_service,
                uow=UowAsyncSession(session)
            )

    @asynccontextmanager
    async def method_creator(self) -> AsyncContextManager[AddMethod]:
        async with self.db_connection_pool() as session:
            yield AddMethod(
                method_db_gateway=MethodGateway(session),
                method_service=self.method_service,
                uow=UowAsyncSession(session)
            )

    @asynccontextmanager
    async def commission_creator(self) -> AsyncContextManager[AddCommission]:
        async with self.db_connection_pool() as session:
            yield AddCommission(
                commission_db_gateway=CommissionGateway(session),
                commission_service=self.commission_service,
                uow=UowAsyncSession(session)
            )
