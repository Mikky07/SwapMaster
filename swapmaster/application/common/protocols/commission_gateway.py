from abc import abstractmethod
from typing import Protocol

from swapmaster.core.models import Commission, CommissionId


class CommissionWriter(Protocol):
    @abstractmethod
    async def add_commission(self, commission: Commission) -> Commission:
        raise NotImplementedError

    @abstractmethod
    async def is_commission_available(self, value: float) -> bool:
        raise NotImplementedError


class CommissionReader(Protocol):
    @abstractmethod
    async def get_commission(self, commission_id: CommissionId) -> Commission:
        raise NotImplementedError
