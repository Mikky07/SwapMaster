from dataclasses import dataclass

from swapmaster.application.common import UoW
from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.protocols import UserSaver
from swapmaster.core.models import User
from swapmaster.core.services import UserService


@dataclass
class NewUserDTO:
    username: str
    email: str
    hashed_password: str


class Authenticate(Interactor[NewUserDTO, User]):
    def __init__(
            self,
            uow: UoW,
            user_saver: UserSaver,
            user_service: UserService
    ):
        self.user_service = user_service
        self.uow = uow
        self.user_gateway = user_saver

    async def __call__(self, data: NewUserDTO) -> User:
        new_user = self.user_service.create_user(
            email=data.email,
            hashed_password=data.hashed_password,
            username=data.username
        )
        user = await self.user_gateway.create_user(user=new_user)
        await self.uow.commit()
        return user
