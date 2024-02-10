import logging

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from starlette import status

from swapmaster.application.create_method import NewMethodDTO, AddMethod
from swapmaster.core.models import Method
from swapmaster.core.utils import exceptions


logger = logging.getLogger(__name__)


async def add_method(
    data: NewMethodDTO,
    interactor: AddMethod = Depends(),
) -> Method:
    try:
        new_method = await interactor(data=data)
    except exceptions.AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=str(e)
        )
    return new_method


# async def get_all_methods() -> list[Method]:
#     ...


def setup_method() -> APIRouter:
    method_router = APIRouter(prefix="/methods")
    method_router.add_api_route(path="", endpoint=add_method, methods=["POST"])

    return method_router
