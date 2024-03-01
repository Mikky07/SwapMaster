import logging
from datetime import datetime, timedelta

import jwt
from fastapi import Depends
from starlette import status
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.exc import NoResultFound

from swapmaster.application.common.db.user_gateway import UserReader
from swapmaster.core.models import User
from swapmaster.core.models.token import Token
from swapmaster.core.utils.exceptions import SMError, UserNotFound
from swapmaster.presentation.api.config.models.auth import AuthConfig
from swapmaster.presentation.api.depends.stub import Stub

logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer("/auth/token")


class AuthProvider:
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
            form_data: OAuth2PasswordRequestForm,
            user_reader: UserReader
    ) -> Token:
        auth_incorrect = SMError("Incorrect username or password")
        try:
            user = await user_reader.get_user_by_username(username=form_data.username)
        except NoResultFound:
            raise auth_incorrect
        if not self.compare_passwords(form_data.password, user.hashed_password):
            raise auth_incorrect
        new_token = self.create_token(user=user)
        return new_token

    async def get_current_user(
            self,
            token=Depends(oauth2_scheme),
            user_reader: UserReader = Depends(Stub(UserReader))
    ) -> User:
        recognition_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Something went wrong with jwt validation"
        )
        try:
            payload = jwt.decode(
                jwt=token,
                key=self.config.secret_key,
                algorithms=[self.algorithm]
            )
            user_id = payload.get("user_id")
            expires_datetime = datetime.fromtimestamp(payload.get("exp"))
            if not user_id:
                raise recognition_error
            if not expires_datetime or expires_datetime < datetime.now():
                raise recognition_error
        except Exception:
            raise
        try:
            user = await user_reader.get_user(user_id=user_id)
        except UserNotFound:
            raise recognition_error
        return user

    def create_access_token(self, user: User) -> str:
        expires_datetime = datetime.now() + timedelta(minutes=self.config.expire_minutes)
        token_payload = {
            "sub": "auth",
            "exp": expires_datetime,
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
