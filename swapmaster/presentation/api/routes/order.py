import logging

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from starlette import status

from swapmaster.application.common.protocols.order_gateway import OrderReader
from swapmaster.application.create_order import NewOrderDTO, AddOrder
from swapmaster.application.finish_order import FinishOrder
from swapmaster.application.get_full_order import GetFullOrder
from swapmaster.core.constants import OrderStatusEnum
from swapmaster.core.models import Order, OrderId, OrderWithRequisites
from swapmaster.core.utils import exceptions
from swapmaster.presentation.api.depends.stub import Stub

logger = logging.getLogger(__name__)


async def add_order(
    data: NewOrderDTO,
    interactor: AddOrder = Depends(),
) -> Order:
    try:
        new_order = await interactor(data=data)
    except exceptions.AlreadyExists as e:
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
        interactor: GetFullOrder = Depends()
) -> OrderWithRequisites:
    order_with_requisites = await interactor(data=order_id)
    return order_with_requisites


async def finish_order(
        order_id: OrderId,
        interactor: FinishOrder = Depends()
) -> Order:
    order_finished = await interactor(data=order_id)
    return order_finished


def setup_order() -> APIRouter:
    order_router = APIRouter(prefix="/orders")
    order_router.add_api_route("", endpoint=add_order, methods=["POST"])
    order_router.add_api_route("", endpoint=get_all_orders, methods=["GET"])
    order_router.add_api_route("/{order_id}", endpoint=get_full_order_information, methods=["GET"])
    order_router.add_api_route("/{order_id}", endpoint=finish_order, methods=["PATCH"])

    return order_router
