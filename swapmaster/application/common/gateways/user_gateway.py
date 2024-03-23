from abc import abstractmethod
from typing import Protocol

from swapmaster.core.models.user import UserId, User


class UserReader(Protocol):
    @abstractmethod
    async def get_user_by_id(self, user_id: UserId) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User:
        raise NotImplementedError


class UserUpdater(Protocol):
    @abstractmethod
    async def update_verification_status(self, user_id: UserId) -> User:
        raise NotImplementedError


class UserSaver(Protocol):
    @abstractmethod
    async def add_user(self, user: User) -> User:
        raise NotImplementedError
