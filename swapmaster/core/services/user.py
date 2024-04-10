import re

from passlib.context import CryptContext

from swapmaster.core.constants import VerificationStatusEnum
from swapmaster.core.models import User
from swapmaster.core.utils.exceptions import SMError


class UserService:
    def __init__(self):
        self.crypt_context = CryptContext(schemes=["bcrypt"])

    def is_email_correct(self, email_address: str):
        if not re.match(
            "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
            email_address
        ):
            raise SMError("Email {email} is not correct!".format(email=email_address))

    def get_password_hash(self, password: str) -> str:
        return self.crypt_context.hash(password)

    def create_user(
            self,
            email: str | None,
            password: str | None,
            username: str,
    ) -> User:
        if email:
            self.is_email_correct(email_address=email)
        password_hash = self.get_password_hash(password=password) if password else None
        return User(
            id=None,
            email=email,
            hashed_password=password_hash,
            username=username,
            verification_status=VerificationStatusEnum.UNVERIFIED,
            tg_id=None
        )
