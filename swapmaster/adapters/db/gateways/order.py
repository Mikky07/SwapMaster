from datetime import datetime
from typing import Optional

from sqlalchemy.exc import InternalError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update

from swapmaster.application.common.protocols.order_gateway import OrderWriter, OrderReader, OrderUpdater
from swapmaster.core.constants import OrderStatusEnum
from swapmaster.core.models import Order, OrderId
from swapmaster.adapters.db import models
from swapmaster.core.utils.exceptions import SMError


class OrderGateway(OrderWriter, OrderReader, OrderUpdater):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def finish_order(self, order_id: OrderId, date_finish: datetime) -> Order:
        kwargs = dict(status=OrderStatusEnum.FINISHED, date_finish=date_finish)
        stmt = (
            update(models.Order)
            .values(kwargs)
            .where(models.Order.id == order_id)
            .returning(models.Order)
        )
        finished_order = await self.session.execute(stmt)
        if not (result := finished_order.scalar_one()):
            raise SMError("Order has not been finished")
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

    async def get_orders_list(self, status: Optional[OrderStatusEnum]) -> list[Order]:
        stmt = select(models.Order)
        if status:
            stmt = stmt.where(models.Order.status == status)
        orders = await self.session.scalars(stmt)
        return [
            Order(
                order_id=order.id,
                pair_id=order.pair_id,
                user_id=order.user_id,
                to_receive=order.to_receive,
                to_send=order.to_send,
                date_start=order.date_start,
                date_finish=order.date_finish,
                status=order.status
            )
            for order in orders.all()
        ]

    async def get_by_id(self, order_id: OrderId) -> Order:
        stmt = select(models.Order).where(models.Order.id == order_id)
        order = await self.session.scalars(stmt)
        if not (result := order.first()):
            raise NoResultFound
        return result

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
