import logging
from dataclasses import dataclass

from swapmaster.application.common.course_obtainer import CourseObtainer
from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.protocols.commission_gateway import CommissionReader
from swapmaster.core.models import PairId
from swapmaster.application.common.protocols.pair_gateway import PairReader
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


class CalculateSendTotal(Interactor[CalculateTotalDTO, CalculatedTotalDTO]):
    def __init__(
        self,
        commission_gateway: CommissionReader,
        pair_gateway: PairReader,
        course_obtainer: CourseObtainer
    ):
        self.pair_gateway = pair_gateway
        self.course_obtainer = course_obtainer
        self.commission_gateway = commission_gateway

    async def calculate(
        self,
        data: CalculateTotalDTO
    ) -> CalculatedTotalDTO:
        pair: Pair = await self.pair_gateway.get_pair(
            pair_id=data.pair_id
        )
        pair_currencies = await self.pair_gateway.get_pair_currencies(
            pair_id=pair.pair_id
        )
        course = await self.course_obtainer.obtain(
            pair_currencies=pair_currencies
        )
        commission = await self.commission_gateway.get_commission(commission_id=pair.commission)
        result_course = course + course * commission.value / 100
        result_course = round(result_course, 2)

        return CalculatedTotalDTO(
            pair_id=pair.pair_id,
            to_send_quantity=result_course
        )
