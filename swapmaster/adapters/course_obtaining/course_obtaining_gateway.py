import logging

import aiohttp

from swapmaster.application.common.course_obtainer import CourseObtainer
from swapmaster.core.models.pair import PairCurrencies

logger = logging.getLogger(__name__)


class CourseObtainerGateway(CourseObtainer):
    def __init__(self):
        self.url = "https://binance.com/api/v3/ticker/price?symbol="

    async def obtain(self, pair_currencies: PairCurrencies) -> float:
        pair_str = str(pair_currencies.currency_from.name) + str(pair_currencies.currency_to.name)
        async with aiohttp.request(method="GET", url=self.url + pair_str) as result:
            course = await result.json()
            course = float(course.get("price"))
        return course
