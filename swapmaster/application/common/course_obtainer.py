from abc import abstractmethod

from swapmaster.core.models.pair import PairCurrencies


class CourseObtainer:
    @abstractmethod
    async def obtain(self, pair_currencies: PairCurrencies) -> float:
        raise NotImplementedError
