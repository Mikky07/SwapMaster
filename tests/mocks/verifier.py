from swapmaster.application.common.verifier import Verifier, VerificationCode
from swapmaster.core.models import User


class VerifierMock(Verifier):
    def __init__(self):
        self.verification_code: VerificationCode = ""
        self.verification_started = False
        self.verification_finished = False

    async def start_verification(self, user: User):
        self.verification_started = True

    async def finish_verification(
            self,
            user: User,
            verification_code: VerificationCode,
    ) -> User:
        self.verification_finished = True
        user.verification_status = VerificationStatusEnum.VERIFIED

