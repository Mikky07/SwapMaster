import logging
from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from starlette import status

from swapmaster.application.common.gateways import MethodReader
from swapmaster.application.create_method import NewMethodDTO
from swapmaster.core.models import Method
from swapmaster.core.utils import exceptions
from swapmaster.presentation.web_api import WebInteractorFactory
from swapmaster.presentation.web_api.depends.stub import Stub

logger = logging.getLogger(__name__)


async def add_method(
    data: NewMethodDTO,
    ioc: Annotated[WebInteractorFactory, Depends(Stub(WebInteractorFactory))]
) -> Method:
    async with ioc.method_creator() as create_method:
        try:
            new_method = await create_method(data=data)
        except exceptions.AlreadyExists as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=str(e)
            )
    return new_method


async def get_all_methods(
        method_gateway: Annotated[MethodReader, Depends(Stub(MethodReader))]
) -> list[Method]:
    return await method_gateway.get_method_list()


def setup_method() -> APIRouter:
    method_router = APIRouter(prefix="/methods")
    method_router.add_api_route(path="", endpoint=add_method, methods=["POST"])
    method_router.add_api_route(path="", endpoint=get_all_methods, methods=["GET"])

    return method_router
