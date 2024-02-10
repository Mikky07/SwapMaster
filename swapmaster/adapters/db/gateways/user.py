from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from swapmaster.adapters.db import models
from swapmaster.core.models.user import User, UserId
from swapmaster.application.common.protocols.user_gateway import UserReader, UserSaver


class UserGateway(UserReader, UserSaver):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_user(self, user: User) -> None:
        ...

    async def get_user(self, user_id: UserId) -> User:
        ...

    async def get_user_by_username(self, username: str) -> User:
        stmt = select(models.User).where(models.User.username == username)
        user = await self.session.scalar(stmt)
        if not user:
            raise NoResultFound
        return User(
            user_id=user.id,
            username=user.username,
            hashed_password=user.hashed_password
        )
