import logging

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDBGateway
from swapmaster.adapters.db import models
from swapmaster.application.common.gateways.method_gateway import MethodWriter, MethodReader
from swapmaster.core.models import CurrencyId, MethodId
from swapmaster.core.models.method import Method
from swapmaster.adapters.db.exceptions import exception_mapper

logger = logging.getLogger(__name__)


class MethodGateway(
    BaseDBGateway[models.Method],
    MethodWriter,
    MethodReader
):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Method, session)

    @exception_mapper
    async def get_method_list(self) -> list[Method]:
        methods = await self.get_model_list()
        return [method.to_dto() for method in methods]

    @exception_mapper
    async def add_method(self, method: Method) -> Method:
        saved_method = await self.create_model(name=method.name, currency_id=method.currency_id)
        return saved_method.to_dto()

    @exception_mapper
    async def is_method_available(self, name: str, currency_id: CurrencyId) -> bool:
        result = await self.read_model(
            [
                models.Method.name == name,
                models.Method.currency_id == currency_id
            ]
        )
        return result is None

    @exception_mapper
    async def get_method_by_id(self, method_id: MethodId) -> Method:
        result = await self.read_model(
            [
                models.Method.id == method_id
            ]
        )
        return result.to_dto()

    @exception_mapper
    async def get_methods_for_currency(self, currency_id: CurrencyId) -> list[Method]:
        result = await self.get_model_list([models.Method.currency_id == currency_id])
        return [method.to_dto() for method in result]
