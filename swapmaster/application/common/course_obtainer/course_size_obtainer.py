from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import PairCurrencies


class CourseObtainer(Protocol):
    @abstractmethod
    async def obtain(self, pair_currencies: PairCurrencies) -> float:
        raise NotImplementedError
