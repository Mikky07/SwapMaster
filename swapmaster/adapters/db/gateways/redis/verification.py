import logging

from redis.asyncio.client import Redis

from swapmaster.application.verifier import UserVerificationCash
from swapmaster.core.models import UserId


logger = logging.getLogger(__name__)


class UserVerificationCashImp(UserVerificationCash):
    def __init__(self, redis: Redis, prefix="user-verification:"):
        self.prefix = prefix
        self.redis = redis

    async def save_user_code(self, code: str, user_id: UserId):
        key = self.prefix + str(user_id)
        result = await self.redis.set(key, code)
        logger.info(result)

    async def get_user_code(self, user_id: UserId) -> str:
        key = self.prefix + str(user_id)
        code = await self.redis.get(key)
        return code
