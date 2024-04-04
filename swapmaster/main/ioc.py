from apscheduler import Scheduler, AsyncScheduler
from dishka import Provider, provide, Scope, from_context, alias
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
    CourseGateway,
)
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
from swapmaster.application.common.task_manager import BaseTaskManager, AsyncTaskManager
from swapmaster.application.common.verifier import VerificationCash
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

    sync_scheduler = from_context(provides=Scheduler)
    async_scheduler = from_context(provides=AsyncScheduler)

    sync_task_manager = provide(SyncTaskManager)
    async_task_manager = provide(AsyncTaskManagerImpl)

    sync_task_manager_proto = alias(source=SyncTaskManager, provides=BaseTaskManager)
    async_task_manager_proto = alias(source=AsyncTaskManagerImpl, provides=AsyncTaskManager)


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    pool = from_context(provides=async_sessionmaker[AsyncSession], scope=Scope.APP)

    @provide
    async def get_session(self, pool: async_sessionmaker[AsyncSession]) -> AsyncSession:
        async with pool() as session:
            yield session

    @provide
    async def get_uow(self, session: AsyncSession) -> UoW:
        yield UowAsyncSession(session)

    user_gateway = provide(UserGateway)
    course_gateway = provide(CourseGateway)
    pair_gateway = provide(PairGateway)
    requisite_gateway = provide(RequisiteGateway)
    order_gateway = provide(OrderGateway)
    method_gateway = provide(MethodGateway)
    reserve_gateway = provide(ReserveGateway)
    order_requisite_gateway = provide(OrderRequisiteGateway)
    commission_gateway = provide(CommissionGateway)


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    central_config = from_context(provides=CentralConfig, scope=Scope.APP)
    verification_cash = from_context(provides=VerificationCash)

    @provide
    async def get_authenticator(self) -> CreateUser:
        yield CreateUser

    @provide
    async def get_requisite_creator(self) -> CreateRequisite:
        yield CreateRequisite

    @provide
    async def get_order_creator(self) -> CreateOrder:
        yield CreateOrder

    @provide
    async def get_requisite_creator(self) -> FinishOrder:
        yield FinishOrder

    @provide
    async def get_order_canceler(self) -> CancelOrder:
        yield CancelOrder

    @provide
    async def get_pair_creator(self) -> CreatePair:
        yield CreatePair

    @provide
    async def get_send_total_calculator(self) -> CalculateSendTotal:
        yield CalculateSendTotal

    @provide
    async def get_requisite_creator(self) -> CreateMethod:
        yield CreateMethod

    @provide
    async def get_payer(self) -> SetOrderPaidUp:
        yield SetOrderPaidUp

    @provide
    async def get_commission_creator(self) -> CreateCommission:
        yield CreateRequisite


class WebInteractorProvider(Provider):
    notifier = from_context(provides=Notifier)

    @provide
    async def get_web_verifier(
            self,
            notifier: Notifier,
            cash: VerificationCashImp,
            uow: UoW,
            user_gateway: UserGateway
    ) -> WebVerifier:
        yield WebVerifier(
            notifier=notifier,
            cash=cash,
            uow=uow,
            user_gateway=user_gateway
        )
