from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDBGateway
from swapmaster.adapters.db import models
from swapmaster.core.models.user import User, UserId
from swapmaster.application.common.protocols.user_gateway import UserReader, UserSaver


class UserGateway(BaseDBGateway, UserReader, UserSaver):
    def __init__(self, session: AsyncSession):
        super().__init__(models.User, session)

    async def save_user(self, user: User) -> None:
        ...

    async def get_user(self, user_id: UserId) -> User:
        ...

    async def get_user_by_username(self, username: str) -> User:
        user = await self.read_model(filters=[models.User.username == username])
        return user.to_dto()
