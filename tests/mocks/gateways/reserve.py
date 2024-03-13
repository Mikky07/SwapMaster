from typing import Dict

from swapmaster.application.common.db.reserve_gateway import ReserveWriter
from swapmaster.core.models import ReserveId, Reserve

NEW_RESERVE_ID = ReserveId(1)
NEW_RESERVE_WALLET_ID = None


class ReserveGatewayMock(ReserveWriter):
    def __init__(self):
        self.reserves: Dict[ReserveId, Reserve] = {}

    async def save_reserve(self, reserve: Reserve) -> Reserve:
        reserve.id = NEW_RESERVE_ID
        reserve.wallet_id = NEW_RESERVE_WALLET_ID
        self.reserves[reserve.id] = reserve
        return self.reserves[reserve.id]
