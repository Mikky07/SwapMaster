from collections.abc import AsyncGenerator

from aiohttp import ClientSession
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from swapmaster.adapters.course_obtaining.course_obtaining_gateway import CourseObtainerGateway
from swapmaster.adapters.db.gateways.commission import CommissionGateway
from swapmaster.adapters.db.gateways.currency import CurrencyGateway
from swapmaster.adapters.db.gateways.method import MethodGateway
from swapmaster.adapters.db.gateways.order import OrderGateway
from swapmaster.adapters.db.gateways.pair import PairGateway
from swapmaster.presentation.api.depends.stub import Stub


async def new_db_session(
        pool: async_sessionmaker[AsyncSession]
) -> AsyncGenerator[AsyncSession]:
    async with pool() as session:
        yield session


async def new_method_gateway(
    async_session=Depends(Stub(AsyncSession))
) -> MethodGateway:
    yield MethodGateway(async_session)


async def new_currency_gateway(
    async_session=Depends(Stub(AsyncSession))
) -> CurrencyGateway:
    yield CurrencyGateway(async_session)


async def new_commission_gateway(
    async_session=Depends(Stub(AsyncSession))
) -> CommissionGateway:
    yield CommissionGateway(async_session)


async def new_order_gateway(
    async_session=Depends(Stub(AsyncSession))
) -> CommissionGateway:
    yield OrderGateway(async_session)


async def new_pair_gateway(
    async_session=Depends(Stub(AsyncSession))
) -> PairGateway:
    yield PairGateway(async_session)


async def new_course_obtainer_gateway(
    aiohttp_session=Depends(Stub(ClientSession))
) -> CourseObtainerGateway:
    yield CourseObtainerGateway(aiohttp_session)


async def new_uow(
    async_session=Depends(Stub(AsyncSession))
) -> AsyncSession:
    return async_session
