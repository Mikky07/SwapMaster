import logging
from dataclasses import dataclass

from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.db.commission_gateway import CommissionReader
from swapmaster.core.models import PairId
from swapmaster.application.common.db.pair_gateway import PairReader
from swapmaster.core.models.pair import Pair
from swapmaster.core.utils.exceptions import SMError


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
        pair_gateway: PairReader
    ):
        self.pair_gateway = pair_gateway
        self.commission_gateway = commission_gateway

    async def calculate(
        self,
        data: CalculateTotalDTO
    ) -> CalculatedTotalDTO:
        pair: Pair = await self.pair_gateway.get_pair_by_id(
            pair_id=data.pair_id
        )

        if not pair:
            raise SMError("Some troubles with fetching pair by id")

        course = await self.pair_gateway.obtain_course(course_id=pair.course_id)

        commission = await self.commission_gateway.get_commission(commission_id=pair.commission)
        send_amount = course.value * data.to_receive_quantity
        result_course = send_amount + send_amount * commission.value / 100
        result_course = round(result_course, 2)

        return CalculatedTotalDTO(
            pair_id=data.pair_id,
            to_send_quantity=result_course
        )
