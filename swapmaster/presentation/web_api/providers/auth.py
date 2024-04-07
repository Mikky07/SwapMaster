from dishka import Scope, Provider, provide, from_context
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request

from swapmaster.application.common.gateways.user_gateway import UserReader
from swapmaster.core.models import User
from swapmaster.core.models.token import Token
from swapmaster.presentation.web_api.auth import AuthHandler
from swapmaster.presentation.web_api.config.models.auth import AuthConfig



class AuthProvider(Provider):
    scope = Scope.REQUEST

    request = from_context(provides=Request)
    config = from_context(provides=AuthConfig, scope=Scope.APP)
    auth_handler = provide(AuthHandler, scope=Scope.APP)

    oauth2_scheme = provide(source=OAuth2PasswordBearer("/auth/token"), provides=OAuth2PasswordBearer)

    @provide
    async def get_token(self, oauth2_password_bearer: OAuth2PasswordBearer, request: Request) -> Token:
        token = await oauth2_password_bearer(request=request)
        if token is None:
            return Token('', '')
        return Token(
            token_type='bearer',
            access_token=token
        )

    @provide
    async def get_current_user(
            self,
            auth_handler: AuthHandler,
            token: Token,
            user_reader: UserReader
    ) -> User:
        return await auth_handler.get_current_user(
            user_reader=user_reader,
            token=token
        )