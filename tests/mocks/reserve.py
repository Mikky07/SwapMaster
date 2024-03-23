from typing import Dict

from swapmaster.application.common.gateways.reserve_gateway import ReserveWriter, ReserveReader
from swapmaster.application.common.reserve_obtainer import RemoteReserve
from swapmaster.core.constants import ReserveUpdateMethodEnum
from swapmaster.core.models import ReserveId, Reserve, MethodId


class ReserveGatewayMock(ReserveWriter, ReserveReader):
    def __init__(self):
        self.reserves: Dict[ReserveId, Reserve] = {}

    async def save_reserve(self, reserve: Reserve) -> Reserve:
        max_of_ids = max(self.reserves) if self.reserves else 0
        new_reserve_id = max_of_ids + 1
        reserve.id = new_reserve_id
        self.reserves[reserve.id] = reserve
        return self.reserves[reserve.id]

    async def get_reserve_of_method(self, method_id: MethodId) -> Reserve:
        ...

    async def get_all_remote_reserves(self) -> list[Reserve]:
        remote_reserves = []
        for reserve in self.reserves.values():
            if reserve.update_method == ReserveUpdateMethodEnum.REMOTE:
                remote_reserves.append(reserve)
        return remote_reserves
