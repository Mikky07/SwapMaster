from fastapi import APIRouter, Depends

from swapmaster.application.common.protocols.pair_gateway import PairReader
from swapmaster.application.create_pair import AddPair, NewPairDTO
from swapmaster.core.models import Pair, PairId
from swapmaster.presentation.api.depends.stub import Stub


async def add_pair(
        data: NewPairDTO,
        interactor: AddPair = Depends()
) -> Pair:
    new_pair = await interactor(data=data)
    return new_pair


async def get_pair(
        pair_id: PairId,
        pair_gateway: PairReader = Depends(Stub(PairReader))
) -> Pair:
    pair = await pair_gateway.get_pair(pair_id=pair_id)
    return pair


def setup_pair() -> APIRouter:
    pair_router = APIRouter(prefix="/pairs")
    pair_router.add_api_route("", get_pair, methods=["GET"])
    pair_router.add_api_route("", add_pair, methods=["POST"])

    return pair_router
