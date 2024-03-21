from typing import Dict

from swapmaster.application.common.verifier import VerificationCash
from swapmaster.core.models import UserId
from swapmaster.application.common.verifier import VerificationCode


class VerificationCashMock(VerificationCash):
    def __init__(self):
        self.codes: Dict[str, VerificationCode] = {}
        self.prefix = "test_verification:"

    def get_key(self, user_id: UserId):
        return self.prefix + str(user_id)

    async def delete_code(self, user_id: UserId):
        del self.codes[self.get_key(user_id)]

    async def get_code(self, user_id: UserId) -> str:
        return self.codes[self.get_key(user_id)]

    async def save_code(self, code: VerificationCode, user_id: UserId):
        self.codes[self.get_key(user_id)] = code

    async def is_code_exists(self, user_id: UserId) -> bool:
        return self.codes.get(self.get_key(user_id), False)
