import logging
from functools import partial
from typing import Iterable

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from swapmaster.adapters.db.currency_db import CurrencyGateway
from swapmaster.application.common.method_gateway import MethodWriter
from swapmaster.application.create_method import AddMethod
from swapmaster.core.services.method import MethodService
from swapmaster.adapters.db.method_db import MethodGateway
from swapmaster.presentation.api.depends.stub import Stub

logger = logging.getLogger(__name__)


# get_from https://github.com/Tishka17/fastapi-template/blob/master/src/app/main/di.py#L19-L28
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


def setup_dependencies(app: FastAPI, pool: async_sessionmaker[AsyncSession]):
    method_service = MethodService()

    app.dependency_overrides[CurrencyGateway] = new_currency_gateway
    app.dependency_overrides[MethodWriter] = new_method_gateway
    app.dependency_overrides[AsyncSession] = partial(new_session, pool)
    app.dependency_overrides[MethodService] = lambda: method_service
    set_depends_as_defaults(AddMethod)

    logger.info("dependencies set up!")
