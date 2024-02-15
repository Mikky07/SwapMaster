import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.exc import InternalError

from swapmaster.adapters.db import models
from swapmaster.application.common.protocols.method_gateway import MethodListReader, MethodWriter
from swapmaster.core.models import CurrencyId
from swapmaster.core.models.method import Method

logger = logging.getLogger(__name__)


class MethodGateway(MethodWriter, MethodListReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_method_list(self) -> list[Method]:
        stmt = select(models.Method)
        methods = await self.session.scalars(stmt)
        return [
            Method(
                method_id=method.id,
                reserve=method.reserve_id,
                currency_id=method.currency_id,
                name=method.name
            ) for method in methods.all()
        ]

    async def add_method(self, method: Method) -> Method:
        kwargs = dict(name=method.name, currency_id=method.currency_id)
        stmt = (
            insert(models.Method)
            .values(**kwargs)
            .returning(models.Method)
        )
        saved_method = await self.session.execute(stmt)
        if not (result := saved_method.scalar_one()):
            raise InternalError
        return Method(
            method_id=result.id,
            name=result.name,
            currency_id=result.currency_id,
            reserve=result.reserve_id
        )

    async def is_method_available(self, name: str, currency_id: CurrencyId) -> bool:
        result = await self.session.scalar(
            select(models.Method)
            .where(models.Method.name == name)
            .where(models.Method.currency_id == currency_id)
        )
        return result is None
