import pytest

from swapmaster.application.create_requisite import CreateRequisite, NewRequisiteDTO
from swapmaster.core.models import Pair, PairId, RequisiteId
from swapmaster.core.utils.exceptions import PairNotExists, RequisiteAlreadyExists
from tests.mocks import UoWMock, RequisiteGatewayMock, PairGatewayMock

TEST_REQUISITE_NAME = "Sberbank RUB"
TEST_REQUISITE_PAIR_ID = PairId(1)
TEST_REQUISITE_REGULAR_EXPRESSION = "^3(?:0[0-5]|[68][0-9])[0-9]{11}$"


@pytest.mark.asyncio
async def test_create_requisite(
        uow: UoWMock,
        requisite_gateway: RequisiteGatewayMock,
        pair_gateway: PairGatewayMock
):
    # stub that simulates the pair, which associated with requisite
    pair = Pair(
        id=TEST_REQUISITE_PAIR_ID,
        method_to=1,
        method_from=1,
        commission=1,
        course_id=1,
        reception_wallet=1
    )

    requisite_creator = CreateRequisite(
        uow=uow,
        requisite_gateway=requisite_gateway,
        pair_gateway=pair_gateway
    )

    new_requisite = NewRequisiteDTO(
        name=TEST_REQUISITE_NAME,
        pair_id=TEST_REQUISITE_PAIR_ID,
        regular_expression=TEST_REQUISITE_REGULAR_EXPRESSION
    )

    with pytest.raises(PairNotExists):
        await requisite_creator(data=new_requisite)

    # adding the pair that associated with requisite
    pair_gateway.pairs[TEST_REQUISITE_PAIR_ID] = pair

    created_requisite = await requisite_creator(data=new_requisite)

    with pytest.raises(RequisiteAlreadyExists):
        await requisite_creator(data=new_requisite)

    assert type(created_requisite.id) is RequisiteId
    assert created_requisite.name == TEST_REQUISITE_NAME
    assert created_requisite.pair_id == TEST_REQUISITE_PAIR_ID
    assert created_requisite.regular_expression == TEST_REQUISITE_REGULAR_EXPRESSION
