from unittest.mock import Mock

import pytest

from swapmaster.application.create_reserve import AddReserve, NewReserveDTO
from swapmaster.core.constants import ReserveUpdateMethodEnum
from swapmaster.core.models import Reserve, ReserveId
from tests.mocks import UoWMock
from tests.mocks.gateways import ReserveGatewayMock


NEW_RESERVE_SIZE = 100
NEW_RESERVE_UPDATE_METHOD = ReserveUpdateMethodEnum.LOCAL


@pytest.fixture
def reserve_service() -> Mock:
    reserve_service = Mock()
    reserve_service.create_reserve = Mock(
        return_value=Reserve(
            id=None,
            size=NEW_RESERVE_SIZE,
            update_method=NEW_RESERVE_UPDATE_METHOD,
            wallet_id=None
        )
    )
    return reserve_service


@pytest.mark.asyncio
async def test_create_reserve_(
        uow: UoWMock, reserve_gateway: ReserveGatewayMock, reserve_service: Mock
) -> None:

    reserve_creator = AddReserve(
        uow=uow, reserve_gateway=reserve_gateway, reserve_service=reserve_service
    )

    reserve_created = await reserve_creator(
        NewReserveDTO(
            size=NEW_RESERVE_SIZE,
            update_method=NEW_RESERVE_UPDATE_METHOD,
        )
    )

    assert reserve_created.id
    assert reserve_created.size == NEW_RESERVE_SIZE
    assert reserve_created.update_method == NEW_RESERVE_UPDATE_METHOD
    assert reserve_created.wallet_id is None

    assert uow.committed
