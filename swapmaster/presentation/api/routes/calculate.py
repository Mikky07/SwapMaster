import logging

from fastapi.routing import APIRouter
from fastapi import Depends

from swapmaster.application.calculate_send_total import (
    CalculateSendTotal,
    CalculateTotalDTO,
    CalculatedTotalDTO
)
from swapmaster.presentation.api.models import CalculateData

logger = logging.getLogger(__name__)


async def calculate_send_total(
    data: CalculateData,
    calculator: CalculateSendTotal = Depends()
) -> CalculatedTotalDTO:
    total = await calculator.calculate(
        data=CalculateTotalDTO(
            pair_id=data.pair_id,
            to_receive_quantity=data.to_receive_quantity
        )
    )
    return total


def setup_calculator() -> APIRouter:
    calculator_router = APIRouter(prefix="/calculate")
    calculator_router.add_api_route(path="", endpoint=calculate_send_total, methods=["GET"])

    return calculator_router
