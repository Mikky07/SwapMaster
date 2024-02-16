from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import Requisite, RequisiteId, PairId


class RequisiteReader(Protocol):
    @abstractmethod
    async def get_requisite(self, requisite_id: RequisiteId) -> Requisite:
        raise NotImplementedError

    @abstractmethod
    async def is_requisite_available(self, requisite_id: RequisiteId) -> bool:
        raise NotImplementedError


class RequisiteUpdater(Protocol):
    ...


class RequisiteWriter(Protocol):
    @abstractmethod
    async def add_requisite(self, requisite: Requisite) -> Requisite:
        raise NotImplementedError
