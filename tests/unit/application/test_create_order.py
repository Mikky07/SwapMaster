from datetime import datetime

import pytest
from unittest.mock import Mock

from swapmaster.application.order.create import CreateOrder, NewOrderDTO
from swapmaster.core.constants import OrderPaymentStatusEnum, OrderStatusEnum, ReserveUpdateMethodEnum, \
    VerificationStatusEnum
from swapmaster.core.models import (
    Order,
    OrderId,
    PairId,
    UserId,
    OrderRequisite,
    Requisite,
    RequisiteId, Pair, MethodId, Method, ReserveId, Reserve, User
)
from swapmaster.core.services import OrderService
from swapmaster.core.utils.exceptions import OrderCreationError, RequisitesNotValid
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
    MethodGatewayMock, RequisiteServiceMock,
)

TEST_PAIR_ID = PairId(1)
TEST_USER_ID = UserId(1)
TEST_PAIR_REQUISITE_ID = RequisiteId(1)
TEST_METHOD_TO_ID = MethodId(1)
TEST_METHOD_FROM_ID = MethodId(2)
TEST_RESERVE_ID = ReserveId(1)

TEST_TO_RECEIVE = 100.0
TEST_TO_SEND = 200.0

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
        requisite_service: RequisiteServiceMock,
        method_gateway: MethodGatewayMock,
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
        requisite_service=requisite_service,
        method_gateway=method_gateway
    )

    test_new_order = NewOrderDTO(
        pair_id=TEST_PAIR_ID,
        user_id=TEST_USER_ID,
        to_receive=TEST_TO_RECEIVE,
        to_send=TEST_TO_SEND,
        requisites_filled=TEST_REQUISITES_FILLED
    )

    pair_gateway.pairs[TEST_PAIR_ID] = Pair(
        id=TEST_PAIR_ID,
        method_to_id=TEST_METHOD_TO_ID,
        method_from_id=TEST_METHOD_FROM_ID,
        commission_id=0,
        course_id=0,
        reception_wallet_id=0
    )

    # This reserve value is less that client want to receive
    test_reserve = Reserve(
        id=TEST_RESERVE_ID,
        size=TEST_TO_RECEIVE - 1,
        update_method=ReserveUpdateMethodEnum.LOCAL,
        wallet_id=0
    )

    reserve_gateway.reserves[TEST_RESERVE_ID] = test_reserve

    method_gateway.methods[TEST_METHOD_TO_ID] = Method(
        id=TEST_METHOD_TO_ID,
        reserve_id=TEST_RESERVE_ID,
        currency_id=0,
        name=""
    )

    with pytest.raises(OrderCreationError):
        await order_creator(data=test_new_order)

    # Update reserve value to enough for this order
    test_reserve.size = TEST_TO_RECEIVE + 1

    reserve_gateway.reserves[TEST_RESERVE_ID] = test_reserve

    # Checking case when filled requisites is invalid

    requisite_service.requisites_valid = False

    with pytest.raises(RequisitesNotValid):
        await order_creator(data=test_new_order)

    requisite_service.requisites_valid = True

    # adding order customer which has invoked the order creation, we need an email for notification

    user_gateway.users[TEST_USER_ID] = User(
        id=TEST_USER_ID,
        username="",
        email="test@mail.ru",
        hashed_password="",
        verification_status=VerificationStatusEnum.VERIFIED
    )

    created_order = await order_creator(data=test_new_order)

    assert type(created_order.order.id) is OrderId
    assert len(order_requisite_gateway.orders_requisites.values()) == len(TEST_REQUISITES_FILLED)

    assert notifier.notified
    assert async_task_manager.tasks_planned.get(f"cancel-order:{created_order.order.id}", False)
    assert uow.committed
