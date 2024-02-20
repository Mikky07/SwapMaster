from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import PairId, Pair, MethodId
from swapmaster.core.models.pair import PairCurrencies


class PairReader(Protocol):
    @abstractmethod
    async def get_pair(self, method_from_id: MethodId, method_to_id: MethodId) -> Pair:
        raise NotImplementedError

    @abstractmethod
    async def get_pair_currencies(self, pair_id: PairId) -> PairCurrencies:
        raise NotImplementedError


class PairWriter(Protocol):
    @abstractmethod
    async def add_pair(self, pair: Pair) -> Pair:
        raise NotImplementedError
