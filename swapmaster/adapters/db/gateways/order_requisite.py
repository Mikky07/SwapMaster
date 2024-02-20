from sqlalchemy.ext.asyncio import AsyncSession

from swapmaster.adapters.db import models
from swapmaster.core.models import OrderRequisite, OrderId
from swapmaster.application.common.protocols import OrderRequisiteReader, OrderRequisiteWriter
from .base import BaseDBGateway


class OrderRequisiteGateway(
    BaseDBGateway,
    OrderRequisiteReader,
    OrderRequisiteWriter
):
    def __init__(self, session: AsyncSession):
        super().__init__(models.OrderRequisite, session)

    async def add_order_requisite(self, order_requisite: OrderRequisite) -> OrderRequisite:
        ...

    async def get_order_requisites(self, order_id: OrderId) -> list[OrderRequisite]:
        requisites = await self.get_model_list([models.OrderRequisite.order_id == order_id])
        return [requisite.to_dto() for requisite in requisites]
