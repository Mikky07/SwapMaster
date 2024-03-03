from fastapi import APIRouter, Depends

from swapmaster.application.common.db import RequisiteReader, OrderRequisiteReader
from swapmaster.application.create_requisite import NewRequisiteDTO
from swapmaster.core.models import OrderId, OrderRequisite, PairId, Requisite
from swapmaster.presentation.api.depends.stub import Stub
from swapmaster.presentation.interactor_factory import InteractorFactory


async def add_requisite(
        data: NewRequisiteDTO,
        ioc: InteractorFactory = Depends(Stub(InteractorFactory))
):
    async with ioc.requisite_creator() as create_requisite:
        await create_requisite(data)


async def get_order_requisites(
        order_id: OrderId,
        order_requisite_gateway: OrderRequisiteReader = Depends(Stub(OrderRequisiteReader))
) -> list[OrderRequisite]:
    order_requisites = await order_requisite_gateway.get_order_requisites(order_id)
    return order_requisites


async def get_pair_requisites(
        pair_id: PairId,
        requisite_gateway: RequisiteReader = Depends(Stub(RequisiteReader))
) -> list[Requisite]:
    pair_requisites = await requisite_gateway.get_requisites_of_pair(pair_id=pair_id)
    return pair_requisites


def setup_requisite() -> APIRouter:
    requisite_router = APIRouter(prefix="/requisites")
    requisite_router.add_api_route("", endpoint=add_requisite, methods=["POST"])
    requisite_router.add_api_route("/order/{order_id}", endpoint=get_order_requisites, methods=["GET"])
    requisite_router.add_api_route("/pair/{pair_id}", endpoint=get_pair_requisites, methods=["GET"])
    return requisite_router
