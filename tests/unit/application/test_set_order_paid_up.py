import pytest

from swapmaster.application.common.task_manager import TaskId
from swapmaster.application.order.set_paid_up import SetOrderPaidUp
from swapmaster.core.constants import OrderStatusEnum, OrderPaymentStatusEnum
from swapmaster.core.models import Order, OrderId
from tests.mocks import (
    OrderGatewayMock,
    AsyncTaskManagerMock,
    UoWMock
)


@pytest.mark.asyncio
async def test_set_order_paid_up_(
        uow: UoWMock,
        order_gateway: OrderGatewayMock,
        async_task_manager: AsyncTaskManagerMock,
):
    test_order = Order(
        id=OrderId(1),
        pair_id=0,
        user_id=0,
        to_receive=0.0,
        to_send=0.0,
        date_start=None,
        date_finish=None,
        status=OrderStatusEnum.PROCESSING,
        payment_status=OrderPaymentStatusEnum.UNPAID
    )

    test_task_id = TaskId("cancel-order:" + str(test_order.id))

    order_gateway.orders[test_order.id] = test_order
    async_task_manager.tasks_planned[test_task_id] = ...

    order_paid_up_setter = SetOrderPaidUp(
        uow=uow,
        order_gateway=order_gateway,
        task_manager=async_task_manager
    )

    order_paid_up = await order_paid_up_setter(order_id=test_order.id)

    assert order_paid_up.payment_status == OrderPaymentStatusEnum.PAID
    assert order_gateway.orders[test_order.id].payment_status == OrderPaymentStatusEnum.PAID

    assert not async_task_manager.tasks_planned.get(test_task_id, False)

    assert uow.committed
