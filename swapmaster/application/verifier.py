import logging
import uuid
from typing import Protocol
from abc import abstractmethod

from swapmaster.application.common import Notifier, UoW
from swapmaster.application.common.db import UserUpdater
from swapmaster.core.models import User, UserId
from swapmaster.core.utils.exceptions import AlreadyExists, VerificationFailed


class UserVerificationCash(Protocol):
    @abstractmethod
    async def get_user_code(self, user_id: UserId) -> str:
        raise NotImplementedError

    @abstractmethod
    async def save_user_code(self, code: str, user_id: UserId):
        raise NotImplementedError

    @abstractmethod
    async def is_user_code_exists(self, user_id: UserId) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_code(self, user_id: UserId):
        raise NotImplementedError


logger = logging.getLogger(__name__)


class Verifier:
    def __init__(
            self,
            notifier: Notifier,
            cash: UserVerificationCash,
            uow: UoW,
    ):
        self.notifier = notifier
        self.cash = cash
        self.uow = uow
        # just for test
        self.verification_url = "http://127.0.0.1:8000/users/verify-account/"

    async def start_verification(self, user: User):
        is_user_code_exists = await self.cash.is_user_code_exists(user_id=user.id)
        if is_user_code_exists:
            raise AlreadyExists("User verification code already exists")
        verification_code = str(uuid.uuid4())
        verification_link = self.__create_verification_link(code=verification_code)
        await self.cash.save_user_code(user_id=user.id, code=verification_code)
        self.__notify_user(user=user, verification_link=verification_link)

    async def finish_verification(self, user: User, verification_code: str, user_updater: UserUpdater) -> User:
        exist_verification_code = await self.cash.get_user_code(user_id=user.id)
        if exist_verification_code != verification_code:
            VerificationFailed("User verification code didn't match")
        user_verified = await user_updater.update_verification_status(user_id=user.id)
        await self.uow.commit()
        await self.cash.delete_user_code(user_id=user.id)
        return user_verified

    async def check_code(self, user_id: UserId, code: str) -> bool:
        user_verification_code = await self.cash.get_user_code(user_id=user_id)
        return user_verification_code == code

    def __notify_user(self, user: User, verification_link: str):
        verification_text = self.__create_notification(user=user, link=verification_link)
        self.notifier.notify(
            user=user,
            notification=verification_text,
            subject="Account confirmation"
        )

    def __create_notification(self, user: User, link: str):
        verification_text = (
            "Welcome, {username}!\n"
            "Follow the link to verify your account: "
        ).format(username=user.username) + link
        return verification_text

    def __create_verification_link(self, code: str) -> str:
        return self.verification_url + str(code)
