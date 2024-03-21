from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import CurrencyId
from swapmaster.core.models.method import Method


class MethodReader(Protocol):
    @abstractmethod
    async def get_method_list(self) -> list[Method]:
        raise NotImplementedError


class MethodWriter(Protocol):
    @abstractmethod
    async def add_method(self, method: Method) -> Method:
        raise NotImplementedError