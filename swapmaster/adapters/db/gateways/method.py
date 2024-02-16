import logging

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDBGateway
from swapmaster.adapters.db import models
from swapmaster.application.common.protocols.method_gateway import MethodListReader, MethodWriter
from swapmaster.core.models import CurrencyId
from swapmaster.core.models.method import Method

logger = logging.getLogger(__name__)


class MethodGateway(BaseDBGateway[models.Method], MethodWriter, MethodListReader):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Method, session)

    async def get_method_list(self) -> list[Method]:
        methods = await self.get_model_list()
        return [method.to_dto() for method in methods]

    async def add_method(self, method: Method) -> Method:
        saved_method = await self.create_model(name=method.name, currency_id=method.currency_id)
        return saved_method.to_dto()

    async def is_method_available(self, name: str, currency_id: CurrencyId) -> bool:
        result = await self.read_model(
            [
                models.Method.name == name,
                models.Method.currency_id == currency_id
            ]
        )
        return result is None
