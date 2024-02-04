from sqlalchemy.exc import InternalError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from swapmaster.application.common.protocols.order_gateway import OrderWriter
from swapmaster.core.models import Order
from swapmaster.adapters.db import models


class OrderGateway(OrderWriter):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_order(self, order: Order) -> Order:
        kwargs = dict(
            pair_id=order.pair_id,
            user_id=order.user_id,
            to_receive=order.to_receive,
            to_send=order.to_send,
            date_start=order.date_start
        )
        stmt = (
            insert(models.Order)
            .values(kwargs)
            .returning(models.Order)
        )
        saved_order = await self.session.execute(stmt)
        if not (result := saved_order.scalar_one()):
            raise InternalError
        return Order(
            order_id=result.id,
            pair_id=result.pair_id,
            user_id=result.user_id,
            to_receive=result.to_receive,
            to_send=result.to_send,
            date_start=result.date_start,
            date_finish=result.date_finish,
            status=result.status
        )
