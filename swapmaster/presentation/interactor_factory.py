from typing import AsyncContextManager
from abc import abstractmethod, ABC

from swapmaster.application import (
    AddRequisite,
    AddOrder,
    FinishOrder,
    CancelOrder,
    CalculateSendTotal,
    AddPair,
    AddMethod,
    GetFullOrder,
    CreateCommission, Authenticate
)
from swapmaster.application.cash_verifier import Verifier


class InteractorFactory(ABC):
    @abstractmethod
    async def get_verifier(self) -> AsyncContextManager[Verifier]:
        raise NotImplementedError

    @abstractmethod
    async def get_authenticator(self) -> AsyncContextManager[Authenticate]:
        raise NotImplementedError

    @abstractmethod
    async def requisite_creator(self) -> AsyncContextManager[AddRequisite]:
        raise NotImplementedError

    @abstractmethod
    async def order_creator(self) -> AsyncContextManager[AddOrder]:
        raise NotImplementedError

    @abstractmethod
    async def order_finisher(self) -> AsyncContextManager[FinishOrder]:
        raise NotImplementedError

    @abstractmethod
    async def order_canceler(self) -> AsyncContextManager[CancelOrder]:
        raise NotImplementedError

    @abstractmethod
    async def send_total_calculator(self) -> AsyncContextManager[CalculateSendTotal]:
        raise NotImplementedError

    @abstractmethod
    async def pair_creator(self) -> AsyncContextManager[AddPair]:
        raise NotImplementedError

    @abstractmethod
    async def method_creator(self) -> AsyncContextManager[AddMethod]:
        raise NotImplementedError

    @abstractmethod
    async def full_order_fetcher(self) -> AsyncContextManager[GetFullOrder]:
        raise NotImplementedError

    @abstractmethod
    async def commission_creator(self) -> AsyncContextManager[CreateCommission]:
        raise NotImplementedError

    @abstractmethod
    async def set_order_as_paid(self) -> AsyncContextManager:
        raise NotImplementedError
