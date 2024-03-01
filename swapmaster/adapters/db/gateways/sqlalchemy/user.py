from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_

from swapmaster.core.constants import VerificationStatusEnum
from swapmaster.core.utils.exceptions import AlreadyExists, UserNotFound
from .base import BaseDBGateway
from swapmaster.adapters.db import models
from swapmaster.core.models.user import User, UserId
from swapmaster.application.common.db.user_gateway import UserReader, UserSaver, UserUpdater


class UserGateway(BaseDBGateway, UserReader, UserSaver, UserUpdater):
    def __init__(self, session: AsyncSession):
        super().__init__(models.User, session)

    async def create_user(self, user: User) -> User:
        is_user_exists = await self.is_model_exists([
            or_(
                models.User.username == user.username,
                models.User.email == user.email
            )
        ])
        if is_user_exists:
            raise AlreadyExists("An email or username is not unique for this user!")
        user_saved = await self.create_model(
            hashed_password=user.hashed_password,
            email=user.email,
            username=user.username
        )
        return user_saved.to_dto()

    async def get_user(self, user_id: UserId) -> User:
        try:
            user = await self.read_model([models.User.id == user_id])
        except NoResultFound:
            raise UserNotFound("That user does not exists!")
        return user

    async def get_user_by_username(self, username: str) -> User:
        user = await self.read_model(filters=[models.User.username == username])
        return user.to_dto()

    async def update_verification_status(self, user_id: UserId) -> User:
        verified_user = await self.update_model(
            [models.User.id == user_id],
            verification_status=VerificationStatusEnum.VERIFIED
        )
        return verified_user.to_dto()
