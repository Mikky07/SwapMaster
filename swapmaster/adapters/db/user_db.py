from swapmaster.core.models.user import User, UserId
from swapmaster.application.common.user_gateway import UserReader, UserSaver


class UserGateway(UserReader, UserSaver):
    async def save_user(self, user: User) -> None:
        ...

    async def get_user(self, user_id: UserId) -> User:
        ...
