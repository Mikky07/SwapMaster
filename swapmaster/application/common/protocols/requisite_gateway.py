from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import Requisite, RequisiteId, OrderId


class RequisiteReader(Protocol):
    @abstractmethod
    async def get_requisite(self, requisite_id: RequisiteId) -> Requisite:
        raise NotImplementedError

    @abstractmethod
    async def is_requisite_available(self, requisite_id: RequisiteId) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_requisites_of_order(self, order_id: OrderId) -> list[Requisite]:
        raise NotImplementedError


class RequisiteUpdater(Protocol):
    ...


class RequisiteWriter(Protocol):
    @abstractmethod
    async def add_requisite(self, requisite: Requisite) -> Requisite:
        raise NotImplementedError
