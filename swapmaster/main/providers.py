from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from swapmaster.adapters.db.gateways.sqlalchemy.base import BaseDBGateway
from swapmaster.presentation.api.depends.stub import Stub


def async_session_provider(pool: async_sessionmaker[AsyncSession]):
    async def new_async_session():
        async with pool() as session:
            yield session

    return new_async_session


class DBGatewayProvider[TDBGateway: BaseDBGateway]:
    def __init__(self, gateway: type[TDBGateway]):
        self.gateway = gateway

    async def __call__(
            self,
            async_session=Depends(Stub(AsyncSession))
    ) -> TDBGateway:
        yield self.gateway(async_session)
