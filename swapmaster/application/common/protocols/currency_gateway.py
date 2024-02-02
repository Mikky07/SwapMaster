from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import Currency


class CurrencyListReader(Protocol):
    @abstractmethod
    async def get_currency_list(self) -> list[Currency]:
        raise NotImplementedError
