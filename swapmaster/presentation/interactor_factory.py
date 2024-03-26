from typing import AsyncContextManager
from abc import abstractmethod, ABC

from swapmaster.application import (
    CreateRequisite,
    CreateOrder,
    FinishOrder,
    CancelOrder,
    CalculateSendTotal,
    CreatePair,
    CreateMethod,
    CreateCommission,
    CreateUser
)


class InteractorFactory(ABC):
    @abstractmethod
    async def get_authenticator(self) -> AsyncContextManager[CreateUser]:
        raise NotImplementedError

    @abstractmethod
    async def requisite_creator(self) -> AsyncContextManager[CreateRequisite]:
        raise NotImplementedError

    @abstractmethod
    async def order_creator(self) -> AsyncContextManager[CreateOrder]:
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
    async def pair_creator(self) -> AsyncContextManager[CreatePair]:
        raise NotImplementedError

    @abstractmethod
    async def method_creator(self) -> AsyncContextManager[CreateMethod]:
        raise NotImplementedError

    @abstractmethod
    async def commission_creator(self) -> AsyncContextManager[CreateCommission]:
        raise NotImplementedError

    @abstractmethod
    async def set_order_as_paid(self) -> AsyncContextManager:
        raise NotImplementedError
