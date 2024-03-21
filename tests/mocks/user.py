from typing import Dict

from swapmaster.core.models import User, UserId
from swapmaster.application.common.db.user_gateway import UserSaver


class UserGatewayMock(UserSaver):
    def __init__(self):
        self.users: Dict[UserId, User] = {}

    async def add_user(self, user: User) -> User:
        max_of_ids = max(self.users) if self.users else 0
        new_reserve_id = max_of_ids + 1
        user.id = new_reserve_id
        self.users[user.id] = user
        return self.users[user.id]
