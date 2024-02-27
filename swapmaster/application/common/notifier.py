from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import User


class Notifier(Protocol):
    @abstractmethod
    async def notify(self, user: User, notification: str) -> None:
        raise NotImplementedError
