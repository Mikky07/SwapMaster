from datetime import datetime
from typing import Dict

from swapmaster.application.common.gateways.order_gateway import (
    OrderUpdater,
    OrderReader,
    OrderWriter
)
from swapmaster.core.constants import OrderStatusEnum, OrderPaymentStatusEnum
from swapmaster.core.models import OrderId, Order


class OrderGatewayMock(OrderUpdater, OrderReader, OrderWriter):
    def __init__(self):
        self.orders: Dict[OrderId, Order] = {}

    async def add_order(self, order: Order) -> Order:
        max_of_ids = max(self.orders) if self.orders else 0
        new_pair_id = max_of_ids + 1
        order.id = new_pair_id
        self.orders[order.id] = order
        return self.orders.get(order.id)

    async def get_order(self, order_id: OrderId) -> Order:
        return self.orders[order_id]

    async def get_orders_list(self, status: OrderStatusEnum) -> list[Order]:
        return [
            order for order in self.orders.values() if order.status == status
        ]

    async def set_as_paid(self, order_id: OrderId) -> Order:
        order = self.orders[order_id]
        order.payment_status = OrderPaymentStatusEnum.PAID
        self.orders[order.id] = order
        return order

    async def cancel_order(self, order_id: OrderId, date_canceled: datetime) -> Order:
        order = self.orders[order_id]
        order.status = OrderStatusEnum.CANCELED
        order.date_finish = date_canceled
        self.orders[order_id] = order
        return order

    async def finish_order(self, order_id: OrderId, date_finish: datetime) -> Order:
        order = self.orders[order_id]
        order.status = OrderStatusEnum.FINISHED
        order.date_finish = date_finish
        self.orders[order_id] = order
        return order
