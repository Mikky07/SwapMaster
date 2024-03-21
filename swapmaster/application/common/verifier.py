from typing import Protocol, TypeAlias
from abc import abstractmethod

from swapmaster.core.models import User, UserId

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


class VerificationCash(Protocol):
    @abstractmethod
    async def get_code(self, user_id: UserId) -> str:
        raise NotImplementedError

    @abstractmethod
    async def save_code(self, code: str, user_id: UserId):
        raise NotImplementedError

    @abstractmethod
    async def is_code_exists(self, user_id: UserId) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete_code(self, user_id: UserId):
        raise NotImplementedError
