from abc import abstractmethod
from asyncio import Protocol

from swapmaster.core.models.pair import PairCurrencies


class CourseObtainer(Protocol):
    @abstractmethod
    async def obtain(self, pair_currencies: PairCurrencies) -> float:
        raise NotImplementedError
