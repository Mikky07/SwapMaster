import pytest
import pytest_asyncio
from dishka import Provider, make_async_container, provide, Scope

from swapmaster.application import CreateUser
from tests.mocks.interactors.user import CreateUserMock


class MockProvider(Provider):
    scope = Scope.APP

    user_creator = provide(source=CreateUserMock, provides=CreateUser)


@pytest.fixture(scope="session")
def mock_container():
    container = make_async_container(MockProvider())
    yield container


@pytest_asyncio.fixture
async def user_creator(mock_container):
    return await mock_container.get(CreateUser)
