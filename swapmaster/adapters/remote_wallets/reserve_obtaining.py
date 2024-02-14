import logging

import aiohttp

from swapmaster.application.common.protocols.reserve_size_obtainer import (
    ReserveSizeObtainer,
    ReserveSize,
    RemoteReserve
)


logger = logging.getLogger(__name__)


class ReserveObtainer(ReserveSizeObtainer):
    def __init__(self):
        self.reserve_obtainer_link = 'https://check-crypto-balance-daddy.p.rapidapi.com/{blockchain}/{address}'

    async def obtain_reserves_sizes(self, reserves: list[RemoteReserve]) -> list[ReserveSize]:
        # async with aiohttp.ClientSession() as session:
        #     for reserve in reserves:
        #         async with session.get(
        #                 url=self.reserve_obtainer_link.format(
        #                     blockchain=wallet.blockchain,
        #                     address=wallet.address
        #                 )
        #         ) as result:
        #             ...
        logger.info("Received reserves to obtain their sizes!")
        fake_result = [
            ReserveSize(
                reserve_id=reserve.reserve_id,
                size=103.0
            )
            for reserve in reserves
        ]
        return fake_result
