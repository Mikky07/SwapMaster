from typing import AsyncGenerator

from apscheduler import Scheduler, AsyncScheduler
from dishka import Provider, provide, Scope, from_context, alias
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
from swapmaster.application.common.verifier import VerificationCash, Verifier
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


class RedisVerificationCashProvider(Provider):
    scope = Scope.APP

    redis = from_context(provides=Redis)

    verification_cash = provide(VerificationCashImp)

    verification_cash_abc = alias(source=VerificationCashImp, provides=VerificationCash)


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    pool = from_context(provides=async_sessionmaker[AsyncSession], scope=Scope.APP)

    @provide
    async def get_session(self, pool: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
        async with pool() as session:
            yield session

    @provide
    async def get_uow(self, session: AsyncSession) -> AsyncGenerator[UoW, None]:
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
    async def get_authenticator(
            self,
            verifier: Verifier,
            uow: UoW,
            user_gateway: UserGateway,
            user_service: UserService
    ) -> AsyncGenerator[CreateUser, None]:
        yield CreateUser(
            uow=uow,
            user_gateway=user_gateway,
            user_service=user_service,
            verifier=verifier
        )

    @provide
    async def get_requisite_creator(
            self,
            uow: UoW,
            requisite_gateway: RequisiteGateway,
            pair_gateway: PairGateway,
    ) -> AsyncGenerator[CreateRequisite, None]:
        yield CreateRequisite(
            uow=uow,
            requisite_gateway=requisite_gateway,
            pair_gateway=pair_gateway
        )

    @provide
    async def get_order_creator(
            self,
            uow: UoW,
            task_manager: AsyncTaskManager,
            requisite_gateway: RequisiteGateway,
            user_gateway: UserGateway,
            order_gateway: OrderGateway,
            order_requisite_gateway: OrderRequisiteGateway,
            pair_gateway: PairGateway,
            method_gateway: MethodGateway,
            config: CentralConfig,
            notifier: Notifier,
            order_service: OrderService,
            requisite_service: RequisiteService,
            reserve_gateway: ReserveGateway
    ) -> AsyncGenerator[CreateOrder, None]:
        yield CreateOrder(
            uow=uow,
            requisite_gateway=requisite_gateway,
            pair_gateway=pair_gateway,
            user_gateway=user_gateway,
            order_gateway=order_gateway,
            order_requisite_gateway=order_requisite_gateway,
            method_gateway=method_gateway,
            task_manager=task_manager,
            config=config,
            notifier=notifier,
            order_service=order_service,
            requisite_service=requisite_service,
            reserve_gateway=reserve_gateway
        )

    @provide
    async def get_requisite_creator(
            self,
            uow: UoW,
            user_gateway: UserGateway,
            order_gateway: OrderGateway,
            pair_gateway: PairGateway,
            method_gateway: MethodGateway,
            notifier: Notifier,
            reserve_gateway: ReserveGateway
    ) -> AsyncGenerator[FinishOrder, None]:
        yield FinishOrder(
            uow=uow,
            pair_gateway=pair_gateway,
            user_gateway=user_gateway,
            order_gateway=order_gateway,
            method_gateway=method_gateway,
            notifier=notifier,
            reserve_gateway=reserve_gateway
        )

    @provide
    async def get_order_canceler(
            self,
            uow: UoW,
            user_gateway: UserGateway,
            order_gateway: OrderGateway,
            notifier: Notifier,
    ) -> AsyncGenerator[CancelOrder, None]:
        yield CancelOrder(
            uow=uow,
            order_gateway=order_gateway,
            user_gateway=user_gateway,
            notifier=notifier
        )

    @provide
    async def get_pair_creator(
            self,
            uow: UoW,
            pair_gateway: PairGateway,
    ) -> AsyncGenerator[CreatePair, None]:
        yield CreatePair(
            pair_gateway=pair_gateway,
            uow=uow
        )

    @provide
    async def get_send_total_calculator(
            self,
            commission_gateway: CommissionGateway,
            pair_gateway: PairGateway,
            course_gateway: CourseGateway,
    ) -> AsyncGenerator[CalculateSendTotal, None]:
        yield CalculateSendTotal(
            commission_gateway=commission_gateway,
            pair_gateway=pair_gateway,
            course_gateway=course_gateway
        )

    @provide
    async def get_requisite_creator(
            self,
            uow: UoW,
            method_gateway: MethodGateway
    ) -> AsyncGenerator[CreateMethod, None]:
        yield CreateMethod(
            method_gateway=method_gateway,
            uow=uow
        )

    @provide
    async def get_payer(
            self,
            uow: UoW,
            order_gateway: OrderGateway,
            task_manager: AsyncTaskManager
    ) -> AsyncGenerator[SetOrderPaidUp, None]:
        yield SetOrderPaidUp(
            task_manager=task_manager,
            order_gateway=order_gateway,
            uow=uow
        )

    @provide
    async def get_commission_creator(
            self,
            uow: UoW,
            requisite_gateway: RequisiteGateway,
            pair_gateway: PairGateway,
    ) -> AsyncGenerator[CreateCommission, None]:
        yield CreateRequisite(
            requisite_gateway=requisite_gateway,
            uow=uow,pair_gateway=pair_gateway
        )


class WebInteractorProvider(Provider):
    scope = Scope.REQUEST

    notifier = from_context(provides=Notifier, scope=Scope.APP)

    @provide
    async def get_web_verifier(
            self,
            notifier: Notifier,
            cash: VerificationCash,
            uow: UoW,
            user_gateway: UserGateway
    ) -> AsyncGenerator[Verifier, None]:
        yield WebVerifier(
            notifier=notifier,
            cash=cash,
            uow=uow,
            user_gateway=user_gateway
        )
