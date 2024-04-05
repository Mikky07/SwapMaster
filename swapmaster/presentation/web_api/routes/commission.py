import logging

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi.routing import APIRouter

from swapmaster.application import CreateCommission, NewCommissionDTO
from swapmaster.core.models import Commission

logger = logging.getLogger(__name__)


async def add_commission(
    commission: NewCommissionDTO,
    create_commission: FromDishka[CreateCommission]
) -> Commission:
    new_commission = await create_commission(data=commission)
    return new_commission


async def get_commissions() -> list[Commission]:
    ...


def setup_commission() -> APIRouter:
    commission_router = APIRouter(prefix="/commissions", route_class=DishkaRoute)
    commission_router.add_api_route(path="", endpoint=add_commission, methods=["POST"])

    return commission_router
