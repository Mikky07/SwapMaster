import logging

from aiohttp import ClientSession

from swapmaster.application.common.course_obtainer import CourseObtainer
from swapmaster.core.models.pair import PairCurrencies

logger = logging.getLogger(__name__)


class CourseObtainerGateway(CourseObtainer):
    def __init__(self, session: ClientSession):
        self.session = session

    async def obtain(self, pair_currencies: PairCurrencies) -> float:
        return 1.1
