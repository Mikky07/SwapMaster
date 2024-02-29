import re

from swapmaster.core.constants import VerificationStatusEnum
from swapmaster.core.models import User
from swapmaster.core.utils.exceptions import SMError


class UserService:

    def is_email_correct(self, email_address: str):
        if not re.match(
            "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
            email_address
        ):
            raise SMError("Email {email} is not correct!".format(email=email_address))

    def create_user(
            self,
            email,
            hashed_password,
            username
    ) -> User:
        self.is_email_correct(email_address=email)
        return User(
            id=None,
            email=email,
            hashed_password=hashed_password,
            username=username,
            verification_status=VerificationStatusEnum.UNVERIFIED
        )
