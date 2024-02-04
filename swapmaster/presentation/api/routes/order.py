import logging

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from starlette import status

from swapmaster.application.create_order import NewOrderDTO, AddOrder
from swapmaster.core.models import Order
from swapmaster.core.utils import exceptions


logger = logging.getLogger(__name__)


async def add_order(
    data: NewOrderDTO,
    interactor: AddOrder = Depends(),
) -> Order:
    try:
        new_order = await interactor(data=data)
    except exceptions.AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=str(e)
        )
    return new_order


def setup_order() -> APIRouter:
    order_router = APIRouter(prefix="/orders")
    order_router.add_api_route(path="", endpoint=add_order, methods=["POST"])

    return order_router
