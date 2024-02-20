from fastapi import APIRouter, Depends

from swapmaster.application.common.protocols import OrderRequisiteReader
from swapmaster.application.create_requisite import NewRequisiteDTO, AddRequisite
from swapmaster.core.models import OrderId, OrderRequisite


async def add_requisite(
        data: NewRequisiteDTO,
        interactor: AddRequisite = Depends()
):
    await interactor(data=data)


async def get_order_requisites(
        order_id: OrderId,
        order_requisite_gateway: OrderRequisiteReader = Depends()
) -> list[OrderRequisite]:
    order_requisites = await order_requisite_gateway.get_order_requisites(order_id)
    return order_requisites


def setup_requisite() -> APIRouter:
    requisite_router = APIRouter(prefix="/requisites")
    requisite_router.add_api_route("", endpoint=add_requisite, methods=["POST"])
    requisite_router.add_api_route("/{order_id}", endpoint=get_order_requisites, methods=["GET"])
    return requisite_router
