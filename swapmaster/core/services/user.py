from swapmaster.core.constants import VerificationStatusEnum
from swapmaster.core.models import User


class UserService:
    def create_user(
            self,
            email,
            hashed_password,
            username
    ) -> User:
        return User(
            id=None,
            email=email,
            hashed_password=hashed_password,
            username=username,
            verification_status=VerificationStatusEnum.UNVERIFIED
        )
