from typing import AsyncContextManager
from abc import abstractmethod

from swapmaster.application import Authenticate, AddRequisite, AddOrder, FinishOrder, CancelOrder, CalculateSendTotal, \
    AddPair, AddMethod, GetFullOrder, AddCommission
from swapmaster.application.order.cancel import OrderCancelerFactory
from swapmaster.application.verifier import Verifier


class InteractorFactory(OrderCancelerFactory):
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
    async def commission_creator(self) -> AsyncContextManager[AddCommission]:
        raise NotImplementedError
