from pytest import fixture
from tests.mocks import UoWMock
from tests.mocks import (
    ReserveGatewayMock,
    CommissionGatewayMock
)


@fixture
def reserve_gateway() -> ReserveGatewayMock:
    return ReserveGatewayMock()


@fixture
def commission_gateway() -> CommissionGatewayMock:
    return CommissionGatewayMock()


@fixture
def uow() -> UoWMock:
    return UoWMock()
