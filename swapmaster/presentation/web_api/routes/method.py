import logging

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi.routing import APIRouter

from swapmaster.application.common.gateways import MethodReader
from swapmaster.application.create_method import NewMethodDTO, CreateMethod
from swapmaster.core.models import Method

logger = logging.getLogger(__name__)


async def add_method(
    data: NewMethodDTO,
    create_method: FromDishka[CreateMethod]
) -> Method:
    new_method = await create_method(data=data)
    return new_method


async def get_all_methods(
        method_gateway: FromDishka[MethodReader]
) -> list[Method]:
    all_methods = await method_gateway.get_method_list()
    return all_methods


def setup_method() -> APIRouter:
    method_router = APIRouter(prefix="/methods", route_class=DishkaRoute)
    method_router.add_api_route(path="", endpoint=add_method, methods=["POST"])
    method_router.add_api_route(path="", endpoint=get_all_methods, methods=["GET"])

    return method_router
