from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import (
    Order, OrderId,
    Requisite, RequisiteId,
    OrderRequisite, OrderRequisiteId
)


class OrderRequisiteReader(Protocol):
    @abstractmethod
    async def get_order_requisites(self, order_id: OrderId) -> list[OrderRequisite]:
        raise NotImplementedError


class OrderRequisiteWriter(Protocol):
    @abstractmethod
    async def add_order_requisite(self, order_requisite: OrderRequisite) -> OrderRequisite:
        raise NotImplementedError
