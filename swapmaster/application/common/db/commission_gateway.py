from abc import abstractmethod
from typing import Protocol

from swapmaster.core.models import Commission, CommissionId


class CommissionWriter(Protocol):
    @abstractmethod
    async def save_commission(self, commission: Commission) -> Commission:
        raise NotImplementedError

    @abstractmethod
    async def is_commission_exists(self, commission: Commission) -> bool:
        raise NotImplementedError


class CommissionReader(Protocol):
    @abstractmethod
    async def get_commission(self, commission_id: CommissionId) -> Commission:
        raise NotImplementedError
