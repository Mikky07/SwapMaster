from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseGateway
from swapmaster.application.common.protocols.order_gateway import OrderWriter, OrderReader, OrderUpdater
from swapmaster.core.constants import OrderStatusEnum
from swapmaster.core.models import Order, OrderId
from swapmaster.adapters.db import models


class OrderGateway(BaseGateway[models.Order], OrderWriter, OrderReader, OrderUpdater):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Order, session)

    async def finish_order(self, order_id: OrderId, date_finish: datetime) -> Order:
        finished_order = await self.update_model(
            status=OrderStatusEnum.FINISHED,
            date_finish=date_finish,
            filters=[models.Order.id == order_id]
        )
        return finished_order.to_dto()

    async def get_orders_list(self, status: Optional[OrderStatusEnum]) -> list[Order]:
        filters = [models.Order.status == status] if status else None
        orders = await self.get_model_list(filters=filters)
        return [order.to_dto() for order in orders]

    async def get_by_id(self, order_id: OrderId) -> Order:
        order = await self.read_model([models.Order.id == order_id])
        return order

    async def add_order(self, order: Order) -> Order:
        result = await self.create_model(
            pair_id=order.pair_id,
            user_id=order.user_id,
            to_receive=order.to_receive,
            to_send=order.to_send,
            date_start=order.date_start
        )
        return result.to_dto()
