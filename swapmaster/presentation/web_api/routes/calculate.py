import logging

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi.routing import APIRouter

from swapmaster.application.calculate_send_total import (
    CalculateTotalDTO,
    CalculatedTotalDTO, CalculateSendTotal
)
from swapmaster.presentation.web_api.models import CalculateData

logger = logging.getLogger(__name__)


async def calculate_send_total(
    data: CalculateData,
    calculate_send_total_: FromDishka[CalculateSendTotal]
) -> CalculatedTotalDTO:
    total = await calculate_send_total_(
        data=CalculateTotalDTO(
            pair_id=data.pair_id,
            to_receive_quantity=data.to_receive_quantity
        )
    )
    return total


def setup_calculator() -> APIRouter:
    calculator_router = APIRouter(prefix="/calculate", route_class=DishkaRoute)
    calculator_router.add_api_route(path="", endpoint=calculate_send_total, methods=["GET"])

    return calculator_router
