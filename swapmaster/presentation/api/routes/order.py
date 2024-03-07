import logging

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from starlette import status

from swapmaster.application import NewOrderDTO
from swapmaster.application.calculate_send_total import CalculateTotalDTO
from swapmaster.application.common.db import OrderReader
from swapmaster.application.order.cancel import CancelOrderDTO
from swapmaster.application.order.create import CreatedOrderDTO
from swapmaster.core.constants import OrderStatusEnum
from swapmaster.core.models import Order, OrderId, OrderWithRequisites
from swapmaster.core.utils.exceptions import SMError
from swapmaster.presentation.api.depends.stub import Stub
from swapmaster.presentation.api.models.order import NewOrderRequestDTO
from swapmaster.presentation.interactor_factory import InteractorFactory

logger = logging.getLogger(__name__)


async def add_order(
    data: NewOrderRequestDTO,
    ioc: InteractorFactory = Depends(Stub(InteractorFactory)),
) -> CreatedOrderDTO:
    async with ioc.send_total_calculator() as calculate_send_total:
        calculated_to_send = await calculate_send_total(
            data=CalculateTotalDTO(
                pair_id=data.pair_id,
                to_receive_quantity=data.to_receive
            )
        )
    async with ioc.order_creator() as order_creator:
        try:
            new_order = await order_creator(
                data=NewOrderDTO(
                    pair_id=data.pair_id,
                    to_receive=data.to_receive,
                    user_id=data.user_id,
                    requisites=data.requisites,
                    to_send=calculated_to_send.to_send_quantity
                )
            )
        except SMError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=str(e)
            )
    return new_order


async def get_all_orders(
        order_status: OrderStatusEnum = None,
        order_gateway: OrderReader = Depends(Stub(OrderReader))
) -> list[Order]:
    return await order_gateway.get_orders_list(status=order_status)


async def get_full_order_information(
        order_id: OrderId,
        ioc: InteractorFactory = Depends(Stub(InteractorFactory)),
) -> OrderWithRequisites:
    async with ioc.full_order_fetcher() as get_full_order:
        order_with_requisites = await get_full_order(data=order_id)
    return order_with_requisites


async def finish_order(
        order_id: OrderId,
        ioc: InteractorFactory = Depends(Stub(InteractorFactory))
) -> Order:
    async with ioc.order_finisher() as finish_order_:
        order_finished = await finish_order_(data=order_id)
    return order_finished


async def set_order_as_paid(
        order_id: OrderId,
        ioc: InteractorFactory = Depends(Stub(InteractorFactory))
):
    async with ioc.set_order_as_paid() as set_order_as_paid_:
        order_paid = await set_order_as_paid_(order_id=order_id)
    return order_paid


async def cancel_order(
        order_id: OrderId,
        ioc: InteractorFactory = Depends(Stub(InteractorFactory))
) -> Order:
    async with ioc.order_canceler() as cancel_order_:
        canceled_order = await cancel_order_(
            data=CancelOrderDTO(
                order_id=order_id,
                notification=f"Your order {order_id} was canceled."
            )
        )
    return canceled_order


def setup_order() -> APIRouter:
    order_router = APIRouter(prefix="/orders")
    order_router.add_api_route("", endpoint=add_order, methods=["POST"])
    order_router.add_api_route("", endpoint=get_all_orders, methods=["GET"])
    order_router.add_api_route("/{order_id}", endpoint=get_full_order_information, methods=["GET"])
    order_router.add_api_route("/{order_id}", endpoint=finish_order, methods=["PATCH"])
    order_router.add_api_route("/pay-up/{order_id}", endpoint=set_order_as_paid, methods=["PATCH"])
    order_router.add_api_route("/{order_id}", endpoint=cancel_order, methods=["DELETE"])

    return order_router
