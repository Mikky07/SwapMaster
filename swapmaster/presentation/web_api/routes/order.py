import logging

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi.routing import APIRouter

from swapmaster.application import NewOrderDTO, FinishOrder
from swapmaster.application.calculate_send_total import CalculateTotalDTO, CalculateSendTotal
from swapmaster.application.common.gateways import OrderReader
from swapmaster.application.order import SetOrderPaidUp
from swapmaster.application.order.cancel import CancelOrderDTO, CancelOrder
from swapmaster.application.order.create import CreatedOrderDTO, CreateOrder
from swapmaster.core.constants import OrderStatusEnum
from swapmaster.core.models import Order, OrderId
from swapmaster.presentation.web_api.models import NewOrderRequestDTO

logger = logging.getLogger(__name__)


async def create_order(
    data: NewOrderRequestDTO,
    calculate_send_total: FromDishka[CalculateSendTotal],
    create_order_: FromDishka[CreateOrder]
) -> CreatedOrderDTO:
    calculated_to_send = await calculate_send_total(
        data=CalculateTotalDTO(
            pair_id=data.pair_id,
            to_receive_quantity=data.to_receive
        )
    )
    new_order = await create_order_(
        data=NewOrderDTO(
            pair_id=data.pair_id,
            to_receive=data.to_receive,
            user_id=data.user_id,
            requisites_filled=data.requisites,
            to_send=calculated_to_send.to_send_quantity
        )
    )
    return new_order


async def get_all_orders(
        order_gateway: FromDishka[OrderReader],
        order_status: OrderStatusEnum | None = None,
) -> list[Order]:
    all_orders = await order_gateway.get_orders_list(status=order_status)
    return all_orders


async def finish_order(
        order_id: OrderId,
        finish_order_: FromDishka[FinishOrder]
) -> Order:
    order_finished = await finish_order_(data=order_id)
    return order_finished


async def set_order_as_paid(
        order_id: OrderId,
        set_order_as_paid_: FromDishka[SetOrderPaidUp]
):
    order_paid = await set_order_as_paid_(order_id=order_id)
    return order_paid


async def cancel_order(
        order_id: OrderId,
        cancel_order_: FromDishka[CancelOrder]
) -> Order:
    canceled_order = await cancel_order_(
        data=CancelOrderDTO(
            order_id=order_id,
            notification=f"Your order {order_id} was canceled."
        )
    )
    return canceled_order


def setup_order() -> APIRouter:
    order_router = APIRouter(prefix="/orders", route_class=DishkaRoute)
    order_router.add_api_route("", endpoint=create_order, methods=["POST"])
    order_router.add_api_route("", endpoint=get_all_orders, methods=["GET"])
    order_router.add_api_route("/{order_id}", endpoint=finish_order, methods=["PATCH"])
    order_router.add_api_route("/pay-up/{order_id}", endpoint=set_order_as_paid, methods=["PATCH"])
    order_router.add_api_route("/{order_id}", endpoint=cancel_order, methods=["DELETE"])

    return order_router
