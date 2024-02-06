import logging
from dataclasses import dataclass

from swapmaster.application.common.course_obtainer import CourseObtainer
from swapmaster.application.common.interactor import Interactor
from swapmaster.core.models import PairId
from swapmaster.application.common.protocols.pair_gateway import PairReader
from swapmaster.core.models.pair import Pair


@dataclass
class CalculateTotalDTO:
    pair_id: PairId
    to_receive_quantity: float


logger = logging.getLogger(__name__)


class CalculateSendTotal(Interactor[CalculateTotalDTO, Pair]):
    def __init__(
        self,
        pair_gateway: PairReader,
        course_obtainer: CourseObtainer
    ):
        self.pair_gateway = pair_gateway
        self.course_obtainer = course_obtainer

    async def calculate(
        self,
        data: CalculateTotalDTO
    ) -> Pair:
        pair: Pair = await self.pair_gateway.get_pair(
            pair_id=data.pair_id
        )
        pair_currencies = await self.pair_gateway.get_pair_currencies(
            pair_id=pair.pair_id
        )
        await self.course_obtainer.obtain(
            pair_currencies=pair_currencies
        )
        return pair
