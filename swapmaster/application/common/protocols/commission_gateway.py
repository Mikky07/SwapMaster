from abc import abstractmethod
from typing import Protocol

from swapmaster.core.models import Commission


class CommissionWriter(Protocol):
    @abstractmethod
    async def add_commission(self, commission: Commission) -> Commission:
        raise NotImplementedError

    @abstractmethod
    async def is_commission_available(self, value: float) -> bool:
        raise NotImplementedError
