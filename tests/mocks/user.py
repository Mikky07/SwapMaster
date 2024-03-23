from typing import Dict

from swapmaster.core.constants import VerificationStatusEnum
from swapmaster.core.models import User, UserId
from swapmaster.application.common.gateways.user_gateway import (
    UserSaver,
    UserUpdater,
    UserReader
)


class UserGatewayMock(UserSaver, UserUpdater, UserReader):
    def __init__(self):
        self.users: Dict[UserId, User] = {}

    async def add_user(self, user: User) -> User:
        max_of_ids = max(self.users) if self.users else 0
        new_reserve_id = max_of_ids + 1
        user.id = new_reserve_id
        self.users[user.id] = user
        return self.users[user.id]

    async def update_verification_status(self, user_id: UserId) -> User:
        user = self.users[user_id]
        user.verification_status = VerificationStatusEnum.VERIFIED
        return user

    async def get_user_by_id(self, user_id: UserId) -> User:
        ...

    async def get_user_by_username(self, username: str) -> User:
        ...
