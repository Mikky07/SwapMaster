from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from swapmaster.application.common.db.pair_gateway import PairReader
from swapmaster.application.create_pair import AddPair, NewPairDTO
from swapmaster.core.models import Pair, MethodId
from swapmaster.core.utils.exceptions import SMError
from swapmaster.presentation.api.depends.stub import Stub


async def add_pair(
        data: NewPairDTO,
        interactor: AddPair = Depends()
) -> Pair:
    new_pair = await interactor(data=data)

    return new_pair


async def get_pair(
        method_from_id: MethodId,
        method_to_id: MethodId,
        pair_gateway: PairReader = Depends(Stub(PairReader))
) -> Pair:
    try:
        pair = await pair_gateway.get_pair(
            method_from_id=method_from_id,
            method_to_id=method_to_id
        )
    except SMError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=str(e)
        )
    return pair


def setup_pair() -> APIRouter:
    pair_router = APIRouter(prefix="/pairs")
    pair_router.add_api_route("", endpoint=add_pair, methods=["POST"])
    pair_router.add_api_route("", endpoint=get_pair, methods=["GET"])

    return pair_router
