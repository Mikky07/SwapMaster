from logging import Logger
from typing import AsyncGenerator

from apscheduler import Scheduler, AsyncScheduler
from adaptix import Retort
from dishka import Provider, provide, Scope, from_context, alias, AnyOf
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from swapmaster.adapters.db.gateways.redis import VerificationCashImp
from swapmaster.adapters.db.gateways.sqlalchemy import (
    UserGateway,
    RequisiteGateway,
    OrderGateway,
    PairGateway,
    OrderRequisiteGateway,
    ReserveGateway,
    CommissionGateway,
    MethodGateway,
    CourseGateway, CurrencyGateway,
)
from swapmaster.adapters.mq.notification import EmailNotifier
from swapmaster.adapters.mq.notification.config import EmailConfig
from swapmaster.adapters.mq.scheduler import SyncTaskManager, AsyncTaskManagerImpl
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
from swapmaster.application.common.gateways import (
    CommissionReader,
    OrderRequisiteReader,
    CourseReader,
    UserReader,
    UserUpdater,
    UserWriter,
    PairReader,
    RequisiteReader,
    OrderReader,
    MethodReader,
    ReserveReader,
    CommissionWriter,
    MethodWriter,
    PairWriter,
    OrderWriter,
    ReserveWriter,
    RequisiteWriter, OrderUpdater, ReserveUpdater, OrderRequisiteWriter, CurrencyListReader,
)
from swapmaster.application.common.task_manager import BaseTaskManager, AsyncTaskManager
from swapmaster.application.common.verifier import VerificationCash, Verifier
from swapmaster.application.get_available_transfer_info import GetAvailableTransferInformation
from swapmaster.application.order import SetOrderPaidUp
from swapmaster.common.config.models.central import CentralConfig
from swapmaster.core.services import (
    UserService,
    OrderService,
    CommissionService,
    RequisiteService
)
from swapmaster.main.db_uow import UowAsyncSession


class ServiceProvider(Provider):
    scope = Scope.APP

    user_service = provide(UserService)
    commission_service = provide(CommissionService)
    order_service = provide(OrderService)
    requisite_service = provide(RequisiteService)


class TaskManagerProvider(Provider):
    scope = Scope.APP

    logger = from_context(provides=Logger)

    @provide
    def get_sync_scheduler(self, logger: Logger) -> Scheduler:
        scheduler = Scheduler(logger=logger)
        return scheduler

    @provide
    async def get_async_scheduler(self, logger: Logger) -> AsyncGenerator[AsyncScheduler, None]:
        scheduler_async = AsyncScheduler(logger=logger)
        async with scheduler_async:
            yield scheduler_async

    sync_task_manager = provide(SyncTaskManager)
    async_task_manager = provide(AsyncTaskManagerImpl)

    sync_task_manager_proto = alias(source=SyncTaskManager, provides=BaseTaskManager)
    async_task_manager_proto = alias(source=AsyncTaskManagerImpl, provides=AsyncTaskManager)


class RedisVerificationCashProvider(Provider):
    scope = Scope.APP

    redis = from_context(provides=Redis)

    verification_cash = provide(VerificationCashImp)

    verification_cash_abc = alias(source=VerificationCashImp, provides=VerificationCash)


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    pool = from_context(provides=async_sessionmaker[AsyncSession], scope=Scope.APP)
    retort = from_context(provides=Retort, scope=scope.APP)

    @provide
    async def get_session(self, pool: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
        async with pool() as session:
            yield session

    @provide
    async def get_uow(self, session: AsyncSession) -> AsyncGenerator[UoW, None]:
        yield UowAsyncSession(session)

    user_gateway = provide(
        source=UserGateway,
        provides=AnyOf[
            UserGateway,
            UserReader,
            UserWriter,
            UserUpdater,
            UserReader | UserWriter
        ]
    )
    course_gateway = provide(
        source=CourseGateway,
        provides=AnyOf[CourseGateway, CourseReader]
    )
    pair_gateway = provide(
        source=PairGateway,
        provides=AnyOf[PairGateway, PairReader, PairWriter]
    )
    requisite_gateway = provide(
        source=RequisiteGateway,
        provides=AnyOf[ReserveGateway, RequisiteReader, RequisiteReader | RequisiteWriter]
    )
    order_gateway = provide(
        source=OrderGateway,
        provides=AnyOf[
            OrderGateway,
            OrderUpdater,
            OrderReader,
            OrderWriter | OrderUpdater,
            OrderUpdater | OrderReader
        ]
    )
    method_gateway = provide(
        source=MethodGateway,
        provides=AnyOf[MethodReader, MethodWriter]
    )
    reserve_gateway = provide(
        source=ReserveGateway,
        provides=AnyOf[ReserveGateway, ReserveReader, ReserveWriter, ReserveUpdater | ReserveReader]
    )
    order_requisite_gateway = provide(
        source=OrderRequisiteGateway,
        provides=AnyOf[OrderRequisiteGateway, OrderRequisiteReader, OrderRequisiteWriter]
    )
    commission_gateway = provide(
        source=CommissionGateway,
        provides=AnyOf[CommissionGateway, CommissionReader, CommissionWriter]
    )
    currency_gateway = provide(
        CurrencyGateway,
        provides=AnyOf[CurrencyListReader]
    )


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    central_config = from_context(provides=CentralConfig, scope=Scope.APP)

    user_creator = provide(CreateUser)
    requisite_creator = provide(CreateRequisite)
    order_creator = provide(CreateOrder)
    order_finisher = provide(FinishOrder)
    order_canceler = provide(CancelOrder)
    pair_creator = provide(CreatePair)
    send_total_calculator = provide(CalculateSendTotal)
    method_creator = provide(CreateMethod)
    payer = provide(SetOrderPaidUp)
    commission_creator = provide(CreateCommission)
    available_transfer_information_fetcher = provide(GetAvailableTransferInformation)


class WebInteractorProvider(Provider):
    scope = Scope.REQUEST

    web_verifier = provide(source=WebVerifier, provides=Verifier)


class EmailNotifierProvider(Provider):
    scope = Scope.APP

    email_config = from_context(provides=EmailConfig)

    email_notifier = provide(source=EmailNotifier, provides=Notifier)
