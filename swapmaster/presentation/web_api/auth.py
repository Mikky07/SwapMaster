import logging
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from sqlalchemy.exc import NoResultFound

from swapmaster.application.common.gateways.user_gateway import UserReader
from swapmaster.core.models import User
from swapmaster.core.models.token import Token
from swapmaster.core.utils.exceptions import AuthFailed, UserNotFound
from swapmaster.presentation.web_api.config.models.auth import AuthConfig

logger = logging.getLogger(__name__)


class AuthHandler:
    def __init__(self, config: AuthConfig):
        self.algorithm = "HS256"
        self.config = config
        self.crypt_context = CryptContext(schemes=["bcrypt"])

    def compare_passwords(self, plain_password: str, hashed_password: str) -> bool:
        return self.crypt_context.verify(plain_password, hashed_password)

    def get_password_hash(self, plain_password):
        return self.crypt_context.hash(secret=plain_password)

    async def auth(
            self,
            username: str,
            password: str,
            user_reader: UserReader
    ) -> Token:
        auth_incorrect = AuthFailed("Incorrect username or password")
        try:
            user = await user_reader.get_user_by_username(username=username)
        except NoResultFound:
            raise auth_incorrect
        if not self.compare_passwords(password, user.hashed_password):
            raise auth_incorrect
        new_token = self.create_token(user=user)
        return new_token

    async def get_current_user(
            self,
            user_reader: UserReader,
            token: Token,
    ) -> User:
        recognition_error = AuthFailed("Something went wrong with jwt validation")
        try:
            payload = jwt.decode(
                jwt=token.access_token,
                key=self.config.secret_key,
                algorithms=[self.algorithm]
            )
            user_id = payload.get("user_id", None)
            expires_datetime = datetime.fromtimestamp(payload.get("exp"))
            if not user_id:
                raise recognition_error
            if not expires_datetime or (expires_datetime <= datetime.now()):
                raise recognition_error
        except Exception:
            raise recognition_error
        try:
            user = await user_reader.get_user_by_id(user_id=user_id)
        except UserNotFound:
            raise recognition_error
        return user

    def create_access_token(self, user: User) -> str:
        expires_datetime = datetime.now(tz=timezone.utc) + timedelta(minutes=self.config.expire_minutes)
        token_payload = {
            "sub": "auth",
            "exp": expires_datetime.timestamp(),
            "user_id": user.id,
        }
        access_token = jwt.encode(
            payload=token_payload,
            key=self.config.secret_key,
            algorithm=self.algorithm
        )
        return access_token

    def create_token(self, user: User) -> Token:
        access_token = self.create_access_token(user=user)
        return Token(access_token=access_token, token_type="bearer")
