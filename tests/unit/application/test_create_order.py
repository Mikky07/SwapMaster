from datetime import datetime

import pytest
from unittest.mock import Mock

from swapmaster.application.order.create import CreateOrder, NewOrderDTO
from swapmaster.core.constants import OrderPaymentStatusEnum, OrderStatusEnum
from swapmaster.core.models import (
    Order,
    OrderId,
    PairId,
    UserId,
    OrderRequisite,
    OrderRequisiteId,
    Requisite,
    RequisiteId
)
from swapmaster.core.services import OrderService
from swapmaster.core.services.requisite import RequisiteService
from tests.mocks import (
    UoWMock,
    OrderGatewayMock,
    UserGatewayMock,
    AsyncTaskManagerMock,
    NotifierMock,
    CentralConfigMock,
    OrderRequisiteGatewayMock,
    PairGatewayMock,
    RequisiteGatewayMock,
    ReserveGatewayMock,
)

TEST_PAIR_ID = PairId(1)
TEST_USER_ID = UserId(1)
TEST_TO_RECEIVE = 100.0
TEST_TO_SEND = 200.0
TEST_PAIR_REQUISITE_ID = RequisiteId(1)

TEST_PAIR_REQUISITES = [
    Requisite(
        id=TEST_PAIR_REQUISITE_ID,
        pair_id=TEST_PAIR_ID,
        name="test_pair_requisite_1",
        regular_expression="test_reqex_1"
    )
]

TEST_REQUISITES_FILLED = [
    OrderRequisite(
        id=None,
        requisite_id=TEST_PAIR_REQUISITE_ID,
        data="test_reqex_1",
        order_id=None
    )
]


@pytest.fixture
def order_service() -> Mock:
    order_service = Mock()
    order_service.create_order = Mock(
        return_value=Order(
            id=None,
            pair_id=TEST_PAIR_ID,
            payment_status=OrderPaymentStatusEnum.UNPAID,
            status=OrderStatusEnum.PROCESSING,
            user_id=TEST_USER_ID,
            to_receive=TEST_TO_RECEIVE,
            to_send=TEST_TO_SEND,
            date_start=datetime.now(),
            date_finish=None
        )
    )

    return order_service


@pytest.mark.asyncio
async def test_create_order_(
        uow: UoWMock,
        order_gateway: OrderGatewayMock,
        user_gateway: UserGatewayMock,
        async_task_manager: AsyncTaskManagerMock,
        notifier: NotifierMock,
        central_config: CentralConfigMock,
        order_requisite_gateway: OrderRequisiteGatewayMock,
        pair_gateway: PairGatewayMock,
        requisite_gateway: RequisiteGatewayMock,
        reserve_gateway: ReserveGatewayMock,
        order_service: OrderService,
        requisite_service: RequisiteService,
):
    order_creator = CreateOrder(
        uow=uow,
        order_gateway=order_gateway,
        user_gateway=user_gateway,
        task_manager=async_task_manager,
        notifier=notifier,
        config=central_config,
        pair_gateway=pair_gateway,
        order_requisite_gateway=order_requisite_gateway,
        requisite_gateway=requisite_gateway,
        reserve_gateway=reserve_gateway,
        order_service=order_service,
        requisite_service=requisite_service
    )

    test_new_order = NewOrderDTO(
        pair_id=TEST_PAIR_ID,
        user_id=TEST_USER_ID,
        to_receive=TEST_TO_RECEIVE,
        to_send=TEST_TO_SEND,
        requisites_filled=TEST_REQUISITES_FILLED
    )

    await order_creator(data=test_new_order)
