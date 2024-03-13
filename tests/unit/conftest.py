from pytest import fixture
from tests.mocks import UoWMock
from tests.mocks.gateways import (
    ReserveGatewayMock
)


@fixture
def reserve_gateway() -> ReserveGatewayMock:
    return ReserveGatewayMock()


@fixture
def uow() -> UoWMock:
    return UoWMock()
