import pytest
from unittest.mock import Mock

from swapmaster.application.create_commission import CreateCommission, NewCommissionDTO
from swapmaster.core.services import CommissionService
from swapmaster.core.utils.exceptions import CommissionIsNotValid, AlreadyExists
from swapmaster.core.models import Commission
from tests.mocks import UoWMock, CommissionGatewayMock


NEW_COMMISSION_VALUE = 1
INCORRECT_COMMISSION_VALUE = -1


@pytest.fixture
def commission_service() -> CommissionService:
    commission_service = Mock()
    commission_service.create_commission = Mock(
        return_value=Commission(
            id=None,
            value=NEW_COMMISSION_VALUE
        )
    )
    return commission_service


def test_create_commission_():
    commission_creator = CommissionService()

    with pytest.raises(CommissionIsNotValid):
        commission_creator.create_commission(value=INCORRECT_COMMISSION_VALUE)

    new_commission: Commission = commission_creator.create_commission(value=NEW_COMMISSION_VALUE)

    assert new_commission.id is None
    assert new_commission.value == NEW_COMMISSION_VALUE


@pytest.mark.asyncio
async def test_add_commission_(
        uow: UoWMock,
        commission_gateway: CommissionGatewayMock,
        commission_service: CommissionService
) -> None:
    new_commission = NewCommissionDTO(
        value=NEW_COMMISSION_VALUE
    )

    duplicate_new_commission = new_commission

    commission_creator = CreateCommission(
        commission_gateway=commission_gateway,
        commission_service=commission_service,
        uow=uow
    )

    created_commission = await commission_creator(data=new_commission)

    with pytest.raises(AlreadyExists):
        await commission_creator(data=duplicate_new_commission)

    assert type(created_commission.id) is int
    assert created_commission.value == NEW_COMMISSION_VALUE

    assert uow.committed
