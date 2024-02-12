from dataclasses import dataclass

from swapmaster.application.common.protocols.reserve_gateway import ReserveReader, ReserveUpdater
from swapmaster.core.models import ReserveId


@dataclass
class RemoteReserve:
    reserve_id: ReserveId
    wallet_address: str


class ReserveRefresh:
    def __init__(
            self,
            reserve_reader: ReserveReader,
            reserve_updater: ReserveUpdater
    ):
        self.reserve_updater = reserve_updater
        self.reserve_reader = reserve_reader

    async def __call__(self):
        reserves = await self.reserve_reader.get_all_remote_reserves()

