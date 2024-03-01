from collections.abc import AsyncGenerator

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from redis.asyncio.client import Redis

from swapmaster.adapters.course_obtaining.course_obtaining_gateway import CourseObtainerGateway
from swapmaster.adapters.db.config.models import RedisConfig
from swapmaster.adapters.db.factory import create_redis
from swapmaster.adapters.db.gateways.redis import UserVerificationCashImp
from swapmaster.adapters.mq.scheduler import TaskSolverImp
from swapmaster.presentation.api.config.models.auth import AuthConfig
from swapmaster.presentation.api.depends.auth import AuthProvider
from swapmaster.presentation.api.depends.stub import Stub
from swapmaster.adapters.db.gateways.sqlalchemy.base import BaseDBGateway


class DBGatewayProvider[TDBGateway: BaseDBGateway]:
    def __init__(self, gateway: type[TDBGateway]):
        self.gateway = gateway

    async def __call__(
            self,
            async_session=Depends(Stub(AsyncSession))
    ) -> TDBGateway:
        yield self.gateway(async_session)


async def new_db_session(
        pool: async_sessionmaker[AsyncSession]
) -> AsyncGenerator[AsyncSession]:
    async with pool() as session:
        yield session


def new_verification_cash(
        redis=Depends(Stub(Redis))
):
    yield UserVerificationCashImp(redis=redis)


def new_course_obtainer_gateway() -> AsyncGenerator[CourseObtainerGateway]:
    yield CourseObtainerGateway()


def new_task_solver(scheduler=Depends(Stub(BackgroundScheduler))):
    yield TaskSolverImp(scheduler=scheduler)


class RedisProvider:
    def __init__(self, config: RedisConfig):
        self.config = config

    async def __call__(self):
        async with create_redis(self.config) as redis:
            yield redis


async def new_uow(
    async_session=Depends(Stub(AsyncSession))
) -> AsyncSession:
    return async_session
