from sqlalchemy.ext.asyncio import AsyncSession

from swapmaster.adapters.db import models
from swapmaster.core.models import OrderId, OrderRequisite
from swapmaster.application.common.gateways import (
    OrderRequisiteReader,
    OrderRequisiteWriter
)
from swapmaster.adapters.db.exceptions import exception_mapper
from .base import BaseDBGateway


class OrderRequisiteGateway(
    BaseDBGateway[models.Requisite],
    OrderRequisiteReader,
    OrderRequisiteWriter
):
    def __init__(self, session: AsyncSession):
        super().__init__(models.OrderRequisite, session)

    @exception_mapper
    async def add_order_requisite(
            self,
            order_requisite: OrderRequisite,
            order_id: OrderId,
    ) -> None:
        await self.create_model(
            order_id=order_id,
            requisite_id=order_requisite.requisite_id,
            data=order_requisite.data
        )

    @exception_mapper
    async def get_order_requisites(self, order_id: OrderId) -> list[OrderRequisite]:
        requisites = await self.get_model_list([models.OrderRequisite.order_id == order_id])
        return [requisite.to_dto() for requisite in requisites]
