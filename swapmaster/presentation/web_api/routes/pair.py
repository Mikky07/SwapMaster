from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from swapmaster.application.common.gateways import PairReader
from swapmaster.application.create_pair import NewPairDTO, CreatePair
from swapmaster.core.models import Pair, MethodId


async def create_pair(
        data: NewPairDTO,
        create_pair_: FromDishka[CreatePair]
) -> Pair:
    new_pair = await create_pair_(data=data)
    return new_pair


async def get_pair(
        method_from_id: MethodId,
        method_to_id: MethodId,
        pair_gateway: FromDishka[PairReader]
) -> Pair:
    pair = await pair_gateway.get_pair(
        method_from_id=method_from_id,
        method_to_id=method_to_id
    )
    return pair


def setup_pair() -> APIRouter:
    pair_router = APIRouter(prefix="/pairs", route_class=DishkaRoute)
    pair_router.add_api_route("", endpoint=create_pair, methods=["POST"])
    pair_router.add_api_route("", endpoint=get_pair, methods=["GET"])

    return pair_router
