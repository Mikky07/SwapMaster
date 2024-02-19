from datetime import datetime
from typing import Protocol
from abc import abstractmethod

from swapmaster.core.constants import OrderStatusEnum
from swapmaster.core.models import Order, OrderId


class OrderReader(Protocol):
    @abstractmethod
    async def get_orders_list(self, status: OrderStatusEnum) -> list[Order]:
        raise NotImplementedError

    @abstractmethod
    async def get_order(self, order_id: OrderId) -> Order:
        raise NotImplementedError


class OrderUpdater(Protocol):
    @abstractmethod
    async def finish_order(self, order_id: OrderId, date_finish: datetime) -> Order:
        raise NotImplementedError


class OrderWriter(Protocol):
    @abstractmethod
    async def add_order(self, order: Order) -> Order:
        raise NotImplementedError
