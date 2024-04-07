from dataclasses import asdict

import pytest

from swapmaster.core.constants import VerificationStatusEnum
from swapmaster.core.models import User
from swapmaster.core.models.token import Token
from swapmaster.core.utils.exceptions import AuthFailed
from swapmaster.presentation.web_api.auth import AuthHandler
from swapmaster.presentation.web_api.config.models.auth import AuthConfig
from tests.mocks import UserGatewayMock


@pytest.mark.asyncio
async def test_auth_handler(
        user_gateway: UserGatewayMock
):
    test_config = AuthConfig(
        secret_key='test-secret',
        expire_minutes=30
    )

    test_user = User(
        id=1,
        username='username',
        email='email@gmail.com',
        hashed_password='hash',
        verification_status=VerificationStatusEnum.VERIFIED
    )

    handler_obj = AuthHandler(
        config=test_config
    )

    test_token_: str = handler_obj.create_access_token(
        user=test_user
    )

    test_token = Token(
        token_type='bearer',
        access_token=test_token_
    )

    # create an expired token
    test_config.expire_minutes = 0
    handler_obj.config = test_config

    expired_token_: str = handler_obj.create_access_token(
        user=test_user
    )

    expired_token = Token(
        token_type='bearer',
        access_token=expired_token_
    )

    # case when user not exists
    with pytest.raises(AuthFailed):
        await handler_obj.get_current_user(
            user_reader=user_gateway,
            token=test_token
        )

    user_gateway.users[test_user.id] = test_user

    # case when token is expired
    with pytest.raises(AuthFailed):
        await handler_obj.get_current_user(
            user_reader=user_gateway,
            token=expired_token
        )

    user_from_token = await handler_obj.get_current_user(
        user_reader=user_gateway,
        token=test_token
    )

    assert asdict(test_user) == asdict(user_from_token)
