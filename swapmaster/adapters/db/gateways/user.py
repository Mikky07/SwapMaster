from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_

from swapmaster.core.utils.exceptions import AlreadyExists
from .base import BaseDBGateway
from swapmaster.adapters.db import models
from swapmaster.core.models.user import User, UserId
from swapmaster.application.common.protocols.user_gateway import UserReader, UserSaver


class UserGateway(BaseDBGateway, UserReader, UserSaver):
    def __init__(self, session: AsyncSession):
        super().__init__(models.User, session)

    async def create_user(self, user: User) -> User:
        is_user_exists = self.is_model_exists([
            or_(
                models.User.username == user.username,
                models.User.email == user.email
            )
        ])
        if is_user_exists:
            raise AlreadyExists("An email or username is not unique for this user!")
        user_saved = await self.create_model(
            id=user.id,
            hashed_password=user.hashed_password,
            email=user.email,
            username=user.username
        )
        return user_saved

    async def get_user(self, user_id: UserId) -> User:
        user = await self.read_model([models.User.id == user_id])
        return user

    async def get_user_by_username(self, username: str) -> User:
        user = await self.read_model(filters=[models.User.username == username])
        return user.to_dto()
