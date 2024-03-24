from datetime import datetime

import pytest

from swapmaster.application.order.finish import FinishOrder
from swapmaster.core.constants import (
    ReserveUpdateMethodEnum,
    OrderStatusEnum,
    OrderPaymentStatusEnum,
    VerificationStatusEnum
)
from swapmaster.core.models import (
    OrderId,
    MethodId,
    ReserveId,
    Order,
    Pair,
    PairId,
    UserId, Reserve, User, Method
)
from tests.mocks import (
    UoWMock,
    OrderGatewayMock,
    UserGatewayMock,
    NotifierMock,
    ReserveGatewayMock,
    PairGatewayMock,
    MethodGatewayMock
)


TEST_ORDER_ID = OrderId(1)
TEST_PAIR_ID = PairId(1)
TEST_USER_ID = UserId(1)
TEST_METHOD_TO_ID = MethodId(1)
TEST_METHOD_FROM_ID = MethodId(2)
TEST_TO_RECEIVE_VALUE = 50.0
TEST_TO_SEND_VALUE = 30.0
TEST_RESERVE_OF_METHOD_TO = Reserve(
    ReserveId(1),
    size=100,
    update_method=ReserveUpdateMethodEnum.LOCAL,
    wallet_id=None
)
TEST_RESERVE_OF_METHOD_FROM = Reserve(
    ReserveId(2),
    size=100,
    update_method=ReserveUpdateMethodEnum.LOCAL,
    wallet_id=None
)


@pytest.mark.asyncio
async def test_finish_order_(
        uow: UoWMock,
        order_gateway: OrderGatewayMock,
        reserve_gateway: ReserveGatewayMock,
        user_gateway: UserGatewayMock,
        pair_gateway: PairGatewayMock,
        method_gateway: MethodGatewayMock,
        notifier: NotifierMock
):
    reserve_gateway.reserves[TEST_RESERVE_OF_METHOD_TO.id] = TEST_RESERVE_OF_METHOD_TO
    reserve_gateway.reserves[TEST_RESERVE_OF_METHOD_FROM.id] = TEST_RESERVE_OF_METHOD_FROM

    test_method_to = Method(
        id=TEST_METHOD_TO_ID,
        reserve_id=TEST_RESERVE_OF_METHOD_TO.id,
        currency_id=0,
        name=""
    )
    test_method_from = Method(
        id=TEST_METHOD_FROM_ID,
        reserve_id=TEST_RESERVE_OF_METHOD_FROM.id,
        currency_id=0,
        name=""
    )
    method_gateway.methods[TEST_METHOD_TO_ID] = test_method_to
    method_gateway.methods[TEST_METHOD_FROM_ID] = test_method_from

    test_pair = Pair(
        id=TEST_PAIR_ID,
        method_to_id=TEST_METHOD_TO_ID,
        method_from_id=TEST_METHOD_FROM_ID,
        commission_id=0,
        course_id=0,
        reception_wallet_id=0
    )

    pair_gateway.pairs[test_pair.id] = test_pair

    test_order = Order(
        id=TEST_ORDER_ID,
        pair_id=TEST_PAIR_ID,
        user_id=TEST_PAIR_ID,
        to_receive=TEST_TO_RECEIVE_VALUE,
        to_send=TEST_TO_SEND_VALUE,
        date_start=None,
        date_finish=None,
        status=OrderStatusEnum.PROCESSING,
        payment_status=OrderPaymentStatusEnum.PAID
    )

    order_gateway.orders[TEST_ORDER_ID] = test_order

    test_user = User(
        id=TEST_ORDER_ID,
        username="",
        email="",
        hashed_password="",
        verification_status=VerificationStatusEnum.VERIFIED
    )

    user_gateway.users[test_user.id] = test_user

    order_finisher = FinishOrder(
        uow=uow,
        order_gateway=order_gateway,
        reserve_gateway=reserve_gateway,
        user_gateway=user_gateway,
        pair_gateway=pair_gateway,
        method_gateway=method_gateway,
        notifier=notifier
    )

    order_finished = await order_finisher(data=TEST_ORDER_ID)

    assert type(order_finished.date_finish) is datetime
    assert order_finished.status == OrderStatusEnum.FINISHED

    assert uow.committed
    assert notifier.notified
