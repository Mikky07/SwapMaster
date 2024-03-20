import pytest

from swapmaster.application.create_pair import NewPairDTO, CreatePair
from tests.mocks import UoWMock, PairGatewayMock

TEST_METHOD_FROM_ID = 1
TEST_METHOD_TO_ID = 2
TEST_COMMISSION_ID = 1
TEST_COURSE_ID = 1
TEST_WALLET_ID = 1


@pytest.mark.asyncio
async def test_create_pair_(uow: UoWMock, pair_gateway: PairGatewayMock):
    new_pair = NewPairDTO(
        method_to=TEST_METHOD_TO_ID,
        method_from=TEST_METHOD_FROM_ID,
        course_id=TEST_COURSE_ID,
        commission=TEST_COMMISSION_ID,
        wallet_id=TEST_WALLET_ID
    )

    pair_creator = CreatePair(
        pair_gateway=pair_gateway,
        uow=uow
    )

    created_pair = await pair_creator(data=new_pair)

    assert type(created_pair.id) is int
    assert created_pair.course_id == TEST_COURSE_ID
    assert created_pair.commission == TEST_COMMISSION_ID
    assert created_pair.method_to == TEST_METHOD_TO_ID
    assert created_pair.method_from == TEST_METHOD_FROM_ID
    assert created_pair.reception_wallet == TEST_WALLET_ID

    assert uow.committed
