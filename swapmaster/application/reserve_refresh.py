import asyncio
import logging

from swapmaster.application.common.protocols.reserve_gateway import ReserveReader, ReserveUpdater
from swapmaster.application.common.protocols.reserve_size_obtainer import ReserveSizeObtainer
from swapmaster.application.common.uow import UoW

logger = logging.getLogger(__name__)


class ReserveRefresh:
    def __init__(
            self,
            uow: UoW,
            reserve_reader: ReserveReader,
            reserve_updater: ReserveUpdater,
            reserve_size_obtainer: ReserveSizeObtainer
    ):
        self.uow = uow
        self.reserve_updater = reserve_updater
        self.reserve_reader = reserve_reader
        self.reserve_size_obtainer = reserve_size_obtainer

    async def __call__(self):
        logger.info("Reserve refresher called!")
        reserves = await self.reserve_reader.get_all_remote_reserves()
        reserve_sizes = await self.reserve_size_obtainer.obtain_reserves_sizes(reserves=reserves)
        tasks_update = [
            self.reserve_updater.update_reserve_size(
                reserve_id=reserve_size.reserve_id,
                size=reserve_size.size
            )
            for reserve_size in reserve_sizes
        ]
        await asyncio.gather(*tasks_update)
        await self.uow.commit()
