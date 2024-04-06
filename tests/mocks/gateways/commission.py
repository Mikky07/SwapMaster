from typing import Dict

from swapmaster.application.common.gateways.commission_gateway import (
    CommissionWriter,
    CommissionReader
)
from swapmaster.core.models import CommissionId, Commission


class CommissionGatewayMock(CommissionWriter, CommissionReader):
    def __init__(self):
        self.commissions: Dict[CommissionId, Commission] = {}

    async def add_commission(self, commission: Commission) -> Commission:
        max_of_ids = max(self.commissions) if self.commissions else 0
        new_commission_id = max_of_ids + 1
        commission.id = new_commission_id
        self.commissions[commission.id] = commission
        return self.commissions[commission.id]

    async def is_commission_exists(self, commission: Commission) -> bool:
        commissions_values = [commission_.value for commission_ in self.commissions.values()]
        return commission.value in commissions_values

    async def get_commission(self, commission_id: CommissionId) -> Commission:
        return self.commissions[commission_id]
