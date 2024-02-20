from dataclasses import dataclass
from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import (
    OrderId,
    RequisiteId,
    OrderRequisite
)


@dataclass
class NewOrderRequisiteDTO:
    requisite_id: RequisiteId
    data: str


class OrderRequisiteReader(Protocol):
    @abstractmethod
    async def get_order_requisites(self, order_id: OrderId) -> list[OrderRequisite]:
        raise NotImplementedError


class OrderRequisiteWriter(Protocol):
    @abstractmethod
    async def add_order_requisite(self, order_requisite: NewOrderRequisiteDTO, order_id: OrderId) -> None:
        raise NotImplementedError
