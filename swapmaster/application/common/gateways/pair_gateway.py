from typing import Protocol, Tuple
from abc import abstractmethod

from swapmaster.core.models import PairId, Pair, MethodId, Commission, Method, Course


class PairReader(Protocol):
    @abstractmethod
    async def get_pair(self, method_from_id: MethodId, method_to_id: MethodId) -> Pair:
        raise NotImplementedError

    @abstractmethod
    async def get_pair_by_id(self, pair_id: PairId) -> Pair | None:
        raise NotImplementedError

    @abstractmethod
    async def get_pair_for_exchange(
            self, method_id: MethodId
    ) -> list[Tuple[PairId, Commission, Method, Course]]:
        raise NotImplementedError


class PairWriter(Protocol):
    @abstractmethod
    async def add_pair(self, pair: Pair) -> Pair:
        raise NotImplementedError
