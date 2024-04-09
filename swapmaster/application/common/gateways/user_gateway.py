from abc import abstractmethod
from typing import Protocol, Any

from swapmaster.core.models.user import UserId, User, ExtraDataId


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


class UserWriter(Protocol):
    @abstractmethod
    async def add_user(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def add_extra_data(self, key: str, value: Any, user_id: UserId) -> None:
        raise NotImplementedError
