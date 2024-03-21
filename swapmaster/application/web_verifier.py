import logging
import uuid

from swapmaster.application.common import Notifier, UoW
from swapmaster.application.common.gateways import UserUpdater
from swapmaster.application.common.verifier import (
    Verifier,
    VerificationCode,
    VerificationCash
)
from swapmaster.core.models import User
from swapmaster.core.utils.exceptions import VerificationFailed


logger = logging.getLogger(__name__)


class WebVerifier(Verifier):
    def __init__(
            self,
            notifier: Notifier,
            cash: VerificationCash,
            uow: UoW,
            user_gateway: UserUpdater,
    ):
        self.user_gateway = user_gateway
        self.notifier = notifier
        self.cash = cash
        self.uow = uow
        self.verification_url = "http://127.0.0.1:8000/users/verify-account/"

    async def start_verification(self, user: User):
        verification_code = VerificationCode(uuid.uuid4())
        verification_link = self.__create_verification_link(code=verification_code)

        await self.cash.save_code(user_id=user.id, code=verification_code)

        self.__notify_user(user=user, verification_link=verification_link)

    async def finish_verification(
            self,
            user: User,
            verification_code: VerificationCode,
    ) -> User:
        exist_verification_code = await self.cash.get_code(user_id=user.id)
        if exist_verification_code != verification_code:
            raise VerificationFailed("User verification code didn't match")

        user_verified = await self.user_gateway.update_verification_status(user_id=user.id)

        await self.uow.commit()
        await self.cash.delete_code(user_id=user.id)

        return user_verified

    def __notify_user(self, user: User, verification_link: str):
        notification_text = (
            f"Welcome, {user.username}!\n"
            f"Follow the link to verify your account: {verification_link}"
        )
        self.notifier.notify(
            user=user,
            notification=notification_text,
            subject="Account confirmation"
        )

    def __create_verification_link(self, code: str) -> str:
        return self.verification_url + str(code)
