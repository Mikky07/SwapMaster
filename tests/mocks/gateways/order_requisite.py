from typing import Dict

from swapmaster.application.common.gateways.order_requisite_gateway import (
    OrderRequisiteReader,
    OrderRequisiteWriter
)
from swapmaster.core.models import OrderRequisiteId, OrderRequisite, OrderId


class OrderRequisiteGatewayMock(OrderRequisiteReader, OrderRequisiteWriter):
    def __init__(self):
        self.orders_requisites: Dict[OrderRequisiteId, OrderRequisite] = {}

    async def get_order_requisites(self, order_id: OrderId) -> list[OrderRequisite]:
        return [
            order_requisite for order_requisite in self.orders_requisites.values()
            if order_requisite.order_id == order_id
        ]

    async def add_order_requisite(self, order_requisite: OrderRequisite, order_id: OrderId) -> None:
        max_of_ids = max(self.orders_requisites) if self.orders_requisites else 0
        new_order_requisite_id = max_of_ids + 1
        order_requisite.id = new_order_requisite_id
        self.orders_requisites[order_requisite.id] = order_requisite
