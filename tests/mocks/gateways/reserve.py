from typing import Dict

from swapmaster.application.common.gateways.reserve_gateway import (
    ReserveWriter,
    ReserveReader,
    ReserveUpdater
)
from swapmaster.core.constants import ReserveUpdateMethodEnum
from swapmaster.core.models import ReserveId, Reserve, WalletId


class ReserveGatewayMock(ReserveWriter, ReserveReader, ReserveUpdater):
    def __init__(self):
        self.reserves: Dict[ReserveId, Reserve] = {}

    async def attach_wallet(self, wallet_id: WalletId, reserve_id: ReserveId) -> Reserve:
        ...

    async def update_reserve_size(self, reserve_id: ReserveId, size: float) -> Reserve:
        reserve = self.reserves[reserve_id]
        reserve.size = size
        self.reserves[reserve_id] = reserve
        return self.reserves[reserve_id]

    async def save_reserve(self, reserve: Reserve) -> Reserve:
        max_of_ids = max(self.reserves) if self.reserves else 0
        new_reserve_id = max_of_ids + 1
        reserve.id = new_reserve_id
        self.reserves[reserve.id] = reserve
        return self.reserves[reserve.id]

    async def get_reserve_by_id(self, reserve_id: ReserveId) -> Reserve:
        return self.reserves[reserve_id]

    async def get_all_remote_reserves(self) -> list[Reserve]:
        remote_reserves = []
        for reserve in self.reserves.values():
            if reserve.update_method == ReserveUpdateMethodEnum.REMOTE:
                remote_reserves.append(reserve)
        return remote_reserves
