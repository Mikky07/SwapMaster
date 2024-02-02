import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from sqlalchemy.exc import InternalError

from swapmaster.adapters.db import models
from swapmaster.application.common.protocols.method_gateway import MethodListReader, MethodWriter
from swapmaster.core.models.method import Method

logger = logging.getLogger(__name__)


class MethodGateway(MethodWriter, MethodListReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_method_list(self) -> list[Method]:
        ...

    async def add_method(self, method: Method) -> Method:
        kwargs = dict(name=method.name, currency_id=method.currency_id)
        stmt = (
            insert(models.Method)
            .values(**kwargs)
            .returning(models.Method)
        )
        logger.info(stmt)
        saved_method = await self.session.execute(stmt)
        if not (result := saved_method.scalar_one()):
            raise InternalError
        return Method(method_id=result.id, name=result.name, currency_id=result.currency_id)
