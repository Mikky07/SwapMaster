import logging

from swapmaster.application.common.course_obtainer import CourseObtainer
from swapmaster.core.models.pair import PairCurrencies

logger = logging.getLogger(__name__)


class StockExchangeObtainerGateway(CourseObtainer):
    def __init__(self):
        ...

    async def obtain(self, pair_currencies: PairCurrencies) -> float:
        logger.info("Stock exchange obtainer called!")
        return 1.1
