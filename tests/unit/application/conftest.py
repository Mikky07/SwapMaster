from pytest import fixture
from tests.mocks import UoWMock, PairGatewayMock, VerifierMock, VerificationCashMock
from tests.mocks import (
    ReserveGatewayMock,
    CommissionGatewayMock,
    RequisiteGatewayMock,
    UserGatewayMock,
    CourseGatewayMock,
    NotifierMock
)


@fixture
def reserve_gateway() -> ReserveGatewayMock:
    return ReserveGatewayMock()


@fixture
def commission_gateway() -> CommissionGatewayMock:
    return CommissionGatewayMock()


@fixture
def user_gateway() -> UserGatewayMock:
    return UserGatewayMock()


@fixture
def notifier() -> NotifierMock:
    return NotifierMock()


@fixture
def verification_cash() -> VerificationCashMock:
    return VerificationCashMock()


@fixture
def verifier() -> VerifierMock:
    return VerifierMock()


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
