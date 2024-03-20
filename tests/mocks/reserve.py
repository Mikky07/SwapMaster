from typing import Dict

from swapmaster.application.common.db.reserve_gateway import ReserveWriter
from swapmaster.core.models import ReserveId, Reserve


class ReserveGatewayMock(ReserveWriter):
    def __init__(self):
        self.reserves: Dict[ReserveId, Reserve] = {}

    async def save_reserve(self, reserve: Reserve) -> Reserve:
        max_of_ids = max(self.reserves) if self.reserves else 0
        new_reserve_id = max_of_ids + 1
        reserve.id = new_reserve_id
        self.reserves[reserve.id] = reserve
        return self.reserves[reserve.id]
