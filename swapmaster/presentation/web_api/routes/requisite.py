from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from swapmaster.application.common.gateways import RequisiteReader, OrderRequisiteReader
from swapmaster.application.create_requisite import NewRequisiteDTO, CreateRequisite
from swapmaster.core.models import OrderId, OrderRequisite, PairId, Requisite


async def create_requisite(
        data: NewRequisiteDTO,
        create_requisite_: FromDishka[CreateRequisite]
) -> Requisite:
    new_order_requisite = await create_requisite_(data)
    return new_order_requisite


async def get_order_requisites(
        order_id: OrderId,
        order_requisite_gateway: FromDishka[OrderRequisiteReader]
) -> list[OrderRequisite]:
    order_requisites = await order_requisite_gateway.get_order_requisites(order_id)
    return order_requisites


async def get_pair_requisites(
        pair_id: PairId,
        requisite_gateway: FromDishka[RequisiteReader]
) -> list[Requisite]:
    pair_requisites = await requisite_gateway.get_requisites_of_pair(pair_id=pair_id)
    return pair_requisites


def setup_requisite() -> APIRouter:
    requisite_router = APIRouter(prefix="/requisites", route_class=DishkaRoute)
    requisite_router.add_api_route("", endpoint=create_requisite, methods=["POST"])
    requisite_router.add_api_route("/order/{order_id}", endpoint=get_order_requisites, methods=["GET"])
    requisite_router.add_api_route("/pair/{pair_id}", endpoint=get_pair_requisites, methods=["GET"])
    return requisite_router
