from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models.method import Method, MethodId


class MethodReader(Protocol):
    @abstractmethod
    async def get_method_list(self) -> list[Method]:
        raise NotImplementedError

    @abstractmethod
    async def get_method_by_id(self, method_id: MethodId) -> Method:
        raise NotImplementedError


class MethodWriter(Protocol):
    @abstractmethod
    async def add_method(self, method: Method) -> Method:
        raise NotImplementedError
