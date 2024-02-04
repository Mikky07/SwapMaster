from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import Order


class OrderWriter(Protocol):
    @abstractmethod
    async def add_order(self, order: Order) -> Order:
        raise NotImplementedError

