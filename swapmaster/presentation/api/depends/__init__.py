import logging
from functools import partial
from typing import Iterable

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from swapmaster.adapters.db.gateways.commission import CommissionGateway
from swapmaster.adapters.db.gateways.currency import CurrencyGateway
from swapmaster.adapters.db.gateways.method import MethodGateway
from swapmaster.application.common.protocols.commission_gateway import CommissionWriter
from swapmaster.application.common.protocols.method_gateway import MethodWriter
from swapmaster.application.create_commission import AddCommission
from swapmaster.application.create_method import AddMethod
from swapmaster.application.common.uow import UoW
from swapmaster.core.services.commission import CommissionService
from swapmaster.core.services.method import MethodService
from swapmaster.presentation.api.depends.stub import Stub

logger = logging.getLogger(__name__)


def set_depends_as_defaults(cls: type) -> None:
    init = cls.__init__
    args_count = init.__code__.co_kwonlyargcount + init.__code__.co_argcount - 1
    init.__defaults__ = tuple(
        Depends() for _ in range(args_count)
    )


async def new_session(
        pool: async_sessionmaker[AsyncSession]
) -> Iterable[AsyncSession]:
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


async def new_uow(
    async_session=Depends(Stub(AsyncSession))
) -> AsyncSession:
    return async_session


def setup_dependencies(
        app: FastAPI,
        pool: async_sessionmaker[AsyncSession]
):
    method_service = MethodService()
    commission_service = CommissionService()

    app.dependency_overrides.update(
        {
            MethodWriter: new_method_gateway,
            CommissionWriter: new_commission_gateway,
            CurrencyGateway: new_currency_gateway,
            AsyncSession: partial(new_session, pool),
            MethodService: lambda: method_service,
            CommissionService: lambda: commission_service,
            UoW: new_uow,
        }
    )

    set_depends_as_defaults(AddMethod)
    set_depends_as_defaults(AddCommission)

    logger.info("dependencies set up!")
