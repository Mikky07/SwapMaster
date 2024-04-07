from unittest.mock import Mock, AsyncMock

import pytest
import pytest_asyncio
from dishka import Provider, make_async_container, provide, Scope, AnyOf

from swapmaster.application import CreateUser
from swapmaster.application.common.gateways import UserReader
from swapmaster.presentation.web_api.auth import AuthHandler
from swapmaster.core.models.token import Token
from tests.mocks import UserGatewayMock
from tests.mocks.interactors.user import CreateUserMock


class MockProvider(Provider):
    scope = Scope.APP

    user_creator = provide(source=CreateUserMock, provides=CreateUser)
    user_gateway = provide(source=UserGatewayMock, provides=AnyOf[UserReader])

    @provide
    def auth_handler(self) -> AuthHandler:
        auth_handler = Mock()
        auth_handler.auth = AsyncMock(
            return_value=Token(token_type="test-type", access_token="test-token")
        )

        return auth_handler


@pytest.fixture(scope='session')
def mock_container():
    container = make_async_container(MockProvider())
    yield container


@pytest_asyncio.fixture
async def user_creator(mock_container):
    return await mock_container.get(CreateUser)


@pytest_asyncio.fixture
async def auth_handler(mock_container):
    return await mock_container.get(AuthHandler)

