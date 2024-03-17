import pytest

from swapmaster.application.create_reserve import CreateReserve, NewReserveDTO
from swapmaster.core.constants import ReserveUpdateMethodEnum
from tests.mocks import UoWMock
from tests.mocks import ReserveGatewayMock


NEW_RESERVE_SIZE = 100
NEW_RESERVE_UPDATE_METHOD = ReserveUpdateMethodEnum.LOCAL


@pytest.mark.asyncio
async def test_create_reserve_(
        uow: UoWMock, reserve_gateway: ReserveGatewayMock
) -> None:

    reserve_creator = CreateReserve(
        uow=uow, reserve_gateway=reserve_gateway
    )

    reserve_created = await reserve_creator(
        NewReserveDTO(
            size=NEW_RESERVE_SIZE,
            update_method=NEW_RESERVE_UPDATE_METHOD,
        )
    )

    assert type(reserve_created.id) is int
    assert reserve_created.size == NEW_RESERVE_SIZE
    assert reserve_created.update_method == NEW_RESERVE_UPDATE_METHOD
    assert reserve_created.wallet_id is None

    assert uow.committed
