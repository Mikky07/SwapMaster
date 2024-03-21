from pytest import fixture
from tests.mocks import UoWMock, PairGatewayMock
from tests.mocks import (
    ReserveGatewayMock,
    CommissionGatewayMock,
    RequisiteGatewayMock
)
from tests.mocks.course import CourseGatewayMock


@fixture
def reserve_gateway() -> ReserveGatewayMock:
    return ReserveGatewayMock()


@fixture
def commission_gateway() -> CommissionGatewayMock:
    return CommissionGatewayMock()


@fixture()
def course_gateway() -> CourseGatewayMock:
    return CourseGatewayMock()


@fixture
def requisite_gateway() -> RequisiteGatewayMock:
    return RequisiteGatewayMock()


@fixture
def pair_gateway() -> PairGatewayMock:
    return PairGatewayMock()


@fixture
def uow() -> UoWMock:
    return UoWMock()
