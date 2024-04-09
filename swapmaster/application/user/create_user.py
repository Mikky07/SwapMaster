from dataclasses import dataclass

from swapmaster.application.common import UoW
from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.gateways.user_gateway import UserWriter
from swapmaster.application.web_verifier import Verifier
from swapmaster.core.constants import VerificationStatusEnum
from swapmaster.core.models import User
from swapmaster.core.services import UserService
from swapmaster.core.utils.exceptions import VerificationFailed


@dataclass
class NewUserDTO:
    username: str
    email: str | None
    password: str | None


class CreateUser(Interactor):
    def __init__(
            self,
            uow: UoW,
            user_gateway: UserWriter,
            user_service: UserService,
            verifier: Verifier
    ):
        self.user_service = user_service
        self.uow = uow
        self.user_gateway = user_gateway
        self.verifier = verifier

    async def __call__(self, data: NewUserDTO) -> User:
        new_user = self.user_service.create_user(
            email=data.email,
            password=data.password,
            username=data.username
        )
        user = await self.user_gateway.add_user(user=new_user)
        await self.uow.commit()
        try:
            await self.verifier.start_verification(user=user)
        except Exception:
            raise VerificationFailed("Some troubles with verification happened")
        return user
