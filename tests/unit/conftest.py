from pytest import fixture

from tests.mocks import (
    PairGatewayMock,
    VerifierMock,
    VerificationCashMock,
    MethodGatewayMock,
    OrderRequisiteGatewayMock,
    OrderGatewayMock, UserGatewayMock
)
from tests.mocks import (
    ReserveGatewayMock,
    CommissionGatewayMock,
    RequisiteGatewayMock,
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
def method_gateway() -> MethodGatewayMock:
    return MethodGatewayMock()


@fixture
def order_gateway() -> OrderGatewayMock:
    return OrderGatewayMock()


@fixture
def order_requisite_gateway() -> OrderRequisiteGatewayMock:
    return OrderRequisiteGatewayMock()


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
def user_gateway() -> UserGatewayMock:
    return UserGatewayMock()
