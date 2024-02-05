import logging

from fastapi.routing import APIRouter
from fastapi import Depends

from swapmaster.application.calculate_send_total import CalculateSendTotal, CalculateTotalDTO
from swapmaster.core.models import Pair
from swapmaster.presentation.api.models import CalculateData
from swapmaster.presentation.api.services.course_obtainer import choose_course_obtainer

logger = logging.getLogger(__name__)


async def calculate_send_total(
    data: CalculateData,
    calculator: CalculateSendTotal = Depends()
) -> Pair:
    pair = await calculator(
        data=CalculateTotalDTO(
            pair_id=data.pair_id,
            to_receive_quantity=data.to_receive_quantity,
            course_obtain_method_chooser=choose_course_obtainer
        )
    )
    return pair


def setup_calculator() -> APIRouter:
    calculator_router = APIRouter(prefix="/calculator")
    calculator_router.add_api_route(path="", endpoint=calculate_send_total, methods=["POST"])

    return calculator_router
