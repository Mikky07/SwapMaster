import logging

from redis.asyncio.client import Redis

from swapmaster.application.cash_verifier import UserVerificationCash
from swapmaster.core.models import UserId


logger = logging.getLogger(__name__)


class UserVerificationCashImp(UserVerificationCash):
    def __init__(self, redis: Redis, prefix="user-verification:"):
        self.prefix = prefix
        self.redis = redis

    def get_key(self, user_id: UserId):
        return self.prefix + str(user_id)

    async def save_user_code(self, code: str, user_id: UserId):
        await self.redis.set(self.get_key(user_id), code)

    async def get_user_code(self, user_id: UserId) -> str:
        code = await self.redis.get(self.get_key(user_id))
        return code

    async def is_user_code_exists(self, user_id: UserId) -> bool:
        is_key_exists = await self.redis.exists(self.get_key(user_id))
        return is_key_exists

    async def delete_user_code(self, user_id: UserId):
        await self.redis.delete(self.get_key(user_id))
