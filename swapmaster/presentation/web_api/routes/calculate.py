import logging
from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Depends

from swapmaster.application.calculate_send_total import (
    CalculateTotalDTO,
    CalculatedTotalDTO
)
from swapmaster.presentation.web_api.depends.stub import Stub
from swapmaster.presentation.web_api.models import CalculateData
from swapmaster.presentation.interactor_factory import InteractorFactory

logger = logging.getLogger(__name__)


async def calculate_send_total(
    data: CalculateData,
    ioc: Annotated[InteractorFactory, Depends(Stub(InteractorFactory))]
) -> CalculatedTotalDTO:
    async with ioc.send_total_calculator() as calculate_send_total_:
        total = await calculate_send_total_(
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
