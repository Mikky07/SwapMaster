import logging
from datetime import datetime, timedelta

from passlib.context import CryptContext
import jwt
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import NoResultFound

from swapmaster.application.common.protocols.user_gateway import UserReader
from swapmaster.core.models import User
from swapmaster.core.models.token import Token
from swapmaster.core.utils.exceptions import SMError
from swapmaster.presentation.api.config.models.auth import AuthConfig

logger = logging.getLogger(__name__)


class AuthProvider:
    def __init__(self, config: AuthConfig, user_gateway: UserReader):
        self.user_gateway = user_gateway
        self.algorithm = "HS256"
        self.config = config
        self.crypt_context = CryptContext(schemes=["bcrypt"])

    def compare_passwords(self, plain_password: str, hashed_password: str) -> bool:
        return self.crypt_context.verify(plain_password, hashed_password)

    def get_password_hash(self, plain_password):
        return self.crypt_context.hash(secret=plain_password)

    async def auth(self, form_data: OAuth2PasswordRequestForm) -> Token:
        auth_incorrect = SMError("Incorrect username or password")
        try:
            user = await self.user_gateway.get_user_by_username(username=form_data.username)
        except NoResultFound:
            raise auth_incorrect
        if not self.compare_passwords(form_data.password, user.hashed_password):
            raise auth_incorrect
        new_token = self.create_token(user=user)
        return new_token

    def create_access_token(self, user: User) -> str:
        expires_datetime = datetime.now() + timedelta(minutes=self.config.expire_minutes)
        token_payload = {
            "sub": "auth",
            "exp": expires_datetime,
            "user_id": user.id,
            "user_password_hash": user.hashed_password
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
