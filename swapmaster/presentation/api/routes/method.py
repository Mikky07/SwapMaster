import logging

from fastapi.routing import APIRouter
from fastapi import Depends

from swapmaster.presentation.api.depends.stub import Stub
from swapmaster.application.create_method import NewMethodDTO, AddMethod
from swapmaster.core.models import Method


logger = logging.getLogger(__name__)


async def add_method(
    data: NewMethodDTO,
    interactor: AddMethod = Depends(),
) -> Method:
    new_method = await interactor(data=data)
    return new_method


def setup_method() -> APIRouter:
    method_router = APIRouter(prefix="/method")
    method_router.add_api_route(path="/new", endpoint=add_method, methods=["POST"])

    return method_router
