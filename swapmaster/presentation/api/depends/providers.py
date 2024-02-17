from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from swapmaster.adapters.course_obtaining.course_obtaining_gateway import CourseObtainerGateway
from swapmaster.presentation.api.depends.stub import Stub
from swapmaster.adapters.db.gateways.base import BaseDBGateway


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


async def new_course_obtainer_gateway() -> AsyncGenerator[CourseObtainerGateway]:
    yield CourseObtainerGateway()


async def new_uow(
    async_session=Depends(Stub(AsyncSession))
) -> AsyncSession:
    return async_session
