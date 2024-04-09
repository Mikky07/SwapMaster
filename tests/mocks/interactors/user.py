from swapmaster.application.user.create_user import NewUserDTO
from swapmaster.core.constants import VerificationStatusEnum
from swapmaster.core.models import User


class CreateUserMock:
    def __init__(self):
        self.called: bool = False

    async def __call__(self, data: NewUserDTO) -> User:
        self.called = True
        return User(
            id=1,
            username=data.username,
            email=data.email,
            hashed_password="hash",
            verification_status=VerificationStatusEnum.UNVERIFIED,
            extra_data_id=1
        )
