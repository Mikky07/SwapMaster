from datetime import datetime

import pytest

from swapmaster.application.order.cancel import CancelOrder, CancelOrderDTO
from swapmaster.core.constants import OrderStatusEnum, OrderPaymentStatusEnum, VerificationStatusEnum
from swapmaster.core.models import Order, OrderId, UserId, User
from tests.mocks import (
    UoWMock,
    OrderGatewayMock,
    UserGatewayMock,
    NotifierMock
)


TEST_ORDER_ID = OrderId(1)
TEST_USER_ID = UserId(1)


@pytest.mark.asyncio
async def test_cancel_order_(
        uow: UoWMock,
        order_gateway: OrderGatewayMock,
        user_gateway: UserGatewayMock,
        notifier: NotifierMock
):
    test_order = Order(
        id=TEST_ORDER_ID,
        pair_id=0,
        user_id=TEST_USER_ID,
        to_receive=0.0,
        to_send=0.0,
        date_start=datetime.now(),
        date_finish=None,
        status=OrderStatusEnum.PROCESSING,
        payment_status=OrderPaymentStatusEnum.PAID
    )

    test_customer = User(
        id=TEST_USER_ID,
        username="",
        email="",
        hashed_password="",
        verification_status=VerificationStatusEnum.VERIFIED,
        tg_id=None
    )

    user_gateway.users[TEST_USER_ID] = test_customer
    order_gateway.orders[TEST_ORDER_ID] = test_order

    order_canceler = CancelOrder(
        uow=uow,
        order_gateway=order_gateway,
        user_gateway=user_gateway,
        notifier=notifier
    )

    to_cancel_order = CancelOrderDTO(
        order_id=TEST_ORDER_ID,
        notification=""
    )

    order_canceled = await order_canceler(data=to_cancel_order)

    assert order_canceled.status == OrderStatusEnum.CANCELED
    assert type(order_canceled.date_finish) is datetime

    assert notifier.notified
    assert uow.committed
