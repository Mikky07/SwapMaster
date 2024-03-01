import logging
import uuid
from typing import Protocol
from abc import abstractmethod

from swapmaster.application.common import Notifier
from swapmaster.core.models import User, UserId


class UserVerificationCash(Protocol):
    @abstractmethod
    async def get_user_code(self, user_id: UserId):
        raise NotImplementedError

    @abstractmethod
    async def save_user_code(self, code: str, user_id: UserId):
        raise NotImplementedError


logger = logging.getLogger(__name__)


class Verifier:
    def __init__(
            self,
            notifier: Notifier,
            cash: UserVerificationCash
    ):
        self.notifier = notifier
        self.cash = cash
        # just for test
        self.verification_url = "http://127.0.0.1:8000/confirm-account/"

    async def start_verification(self, user: User):
        verification_code = str(uuid.uuid4())
        verification_link = self.__create_verification_link(code=verification_code)
        await self.cash.save_user_code(user_id=user.id, code=verification_code)
        self.__notify_user(user=user, verification_link=verification_link)

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
