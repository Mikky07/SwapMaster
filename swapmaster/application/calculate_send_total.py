import logging
from dataclasses import dataclass

from swapmaster.application.common.gateways import CourseReader
from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.gateways.commission_gateway import CommissionReader
from swapmaster.core.models import PairId
from swapmaster.application.common.gateways.pair_gateway import PairReader
from swapmaster.core.models.pair import Pair


@dataclass
class CalculateTotalDTO:
    pair_id: PairId
    to_receive_quantity: float


@dataclass
class CalculatedTotalDTO:
    pair_id: PairId
    to_send_quantity: float


logger = logging.getLogger(__name__)


class CalculateSendTotal(Interactor):
    def __init__(
        self,
        commission_gateway: CommissionReader,
        pair_gateway: PairReader,
        course_gateway: CourseReader,
    ):
        self.course_gateway = course_gateway
        self.pair_gateway = pair_gateway
        self.commission_gateway = commission_gateway

    async def __call__(
        self,
        data: CalculateTotalDTO
    ) -> CalculatedTotalDTO:
        pair: Pair = await self.pair_gateway.get_pair_by_id(
            pair_id=data.pair_id
        )

        course = await self.course_gateway.get_course_by_id(course_id=pair.course_id)
        commission = await self.commission_gateway.get_commission(commission_id=pair.commission_id)

        quantity_on_the_course = course.value * data.to_receive_quantity
        result_course = quantity_on_the_course + quantity_on_the_course * commission.value / 100
        result_course = round(result_course, 2)

        return CalculatedTotalDTO(
            pair_id=data.pair_id,
            to_send_quantity=result_course
        )
