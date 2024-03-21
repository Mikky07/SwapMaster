from typing import Protocol, TypeAlias
from abc import abstractmethod

from swapmaster.core.models import User


VerificationCode: TypeAlias = str


class Verifier(Protocol):
    @abstractmethod
    async def start_verification(self, user: User):
        raise NotImplementedError

    @abstractmethod
    async def finish_verification(
            self,
            user: User,
            verification_code: VerificationCode,
    ) -> User:
        raise NotImplementedError
