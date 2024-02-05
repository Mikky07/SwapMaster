import logging
from dataclasses import dataclass
from typing import Callable

from swapmaster.application.common.course_obtainer import CourseObtainer
from swapmaster.application.common.interactor import Interactor
from swapmaster.core.models import PairId
from swapmaster.application.common.protocols.pair_gateway import PairReader
from swapmaster.core.models.pair import Pair
from swapmaster.core.constants import CourseObtainingMethod


@dataclass
class CalculateTotalDTO:
    pair_id: PairId
    to_receive_quantity: float
    course_obtain_method_chooser: Callable[[CourseObtainingMethod], CourseObtainer]


logger = logging.getLogger(__name__)


class CalculateSendTotal(Interactor[CalculateTotalDTO, Pair]):
    def __init__(
        self,
        pair_gateway: PairReader
    ):
        self.pair_gateway = pair_gateway

    async def __call__(
        self,
        data: CalculateTotalDTO
    ) -> Pair:
        pair: Pair = await self.pair_gateway.get_pair(
            pair_id=data.pair_id
        )
        course_obtainer = data.course_obtain_method_chooser(
            pair.course_obtaining_method
        )
        pair_currencies = await self.pair_gateway.get_pair_currencies(
            pair_id=pair.pair_id
        )
        logger.info(course_obtainer)
        return pair
