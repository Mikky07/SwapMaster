import pytest

from tests.mocks import UserGatewayMock


@pytest.fixture
def user_gateway() -> UserGatewayMock:
    return UserGatewayMock()
