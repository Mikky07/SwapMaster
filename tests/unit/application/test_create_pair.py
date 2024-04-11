import pytest

from swapmaster.application.pair.create_pair import NewPairDTO, CreatePair
from swapmaster.core.models import CommissionId, WalletId, CourseId, MethodId, PairId
from tests.mocks import UoWMock, PairGatewayMock

TEST_METHOD_FROM_ID = MethodId(1)
TEST_METHOD_TO_ID = MethodId(2)
TEST_COMMISSION_ID = CommissionId(1)
TEST_COURSE_ID = CourseId(1)
TEST_WALLET_ID = WalletId(1)


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

    assert type(created_pair.id) is PairId
    assert created_pair.course_id == TEST_COURSE_ID
    assert created_pair.commission_id == TEST_COMMISSION_ID
    assert created_pair.method_to_id == TEST_METHOD_TO_ID
    assert created_pair.method_from_id == TEST_METHOD_FROM_ID
    assert created_pair.reception_wallet_id == TEST_WALLET_ID

    assert uow.committed
