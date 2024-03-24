import pytest

from swapmaster.application.calculate_send_total import (
    CalculateSendTotal,
    CalculateTotalDTO,
)
from swapmaster.core.constants import CourseUpdateMethodEnum
from swapmaster.core.models import (
    PairId,
    Commission,
    Course,
    Pair, MethodId, CourseId, CommissionId, WalletId
)
from tests.mocks import (
    CommissionGatewayMock,
    PairGatewayMock,
    CourseGatewayMock
)


TEST_PAIR_ID = PairId(1)
TEST_TO_RECEIVE_QUANTITY = 100.0
TEST_COMMISSION_VALUE = 10
TEST_COURSE_VALUE = 2


@pytest.mark.asyncio
async def test_calculate_send_total_(
        course_gateway: CourseGatewayMock,
        pair_gateway: PairGatewayMock,
        commission_gateway: CommissionGatewayMock
):
    on_the_course_amount = TEST_COURSE_VALUE * TEST_TO_RECEIVE_QUANTITY
    expected_to_send_quantity = on_the_course_amount + on_the_course_amount * TEST_COMMISSION_VALUE / 100

    # arrange

    course = Course(
        CourseId(0),
        value=TEST_COURSE_VALUE,
        update_method=CourseUpdateMethodEnum.LOCAL
    )
    commission = Commission(
        id=CommissionId(0),
        value=TEST_COMMISSION_VALUE
    )
    pair = Pair(
        TEST_PAIR_ID,
        MethodId(0),
        MethodId(0),
        commission_id=commission.id,
        course_id=course.id,
        reception_wallet_id=WalletId(0)
    )

    pair_gateway.pairs[pair.id] = pair
    course_gateway.courses[course.id] = course
    commission_gateway.commissions[commission.id] = commission

    send_total_calculator = CalculateSendTotal(
        commission_gateway=commission_gateway,
        pair_gateway=pair_gateway,
        course_gateway=course_gateway
    )

    amount_for_calculation = CalculateTotalDTO(
        pair_id=TEST_PAIR_ID,
        to_receive_quantity=TEST_TO_RECEIVE_QUANTITY
    )

    # act

    calculated_amount = await send_total_calculator(data=amount_for_calculation)

    # asserting

    assert calculated_amount.to_send_quantity == expected_to_send_quantity
    assert calculated_amount.pair_id == TEST_PAIR_ID
