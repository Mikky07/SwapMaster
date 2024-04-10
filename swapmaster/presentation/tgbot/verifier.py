from swapmaster.application.common.verifier import Verifier, VerificationCode
from swapmaster.core.models import User


class TGBotVerifier(Verifier):
    async def start_verification(self, user: User):
        ...

    async def finish_verification(
            self,
            user: User,
            verification_code: VerificationCode,
    ) -> User:
        ...
