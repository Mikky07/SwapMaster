from typing import Dict

from swapmaster.application.common.db.commission_gateway import CommissionWriter
from swapmaster.core.models import CommissionId, Commission


class CommissionGatewayMock(CommissionWriter):
    def __init__(self):
        self.commissions: Dict[CommissionId, Commission] = {}

    async def save_commission(self, commission: Commission) -> Commission:
        max_of_ids = max(self.commissions) if self.commissions else 0
        new_commission_id = max_of_ids + 1
        commission.id = new_commission_id
        self.commissions[commission.id] = commission
        return self.commissions[commission.id]

    async def is_commission_exists(self, commission: Commission) -> bool:
        commissions_values = [commission_.value for commission_ in self.commissions.values()]
        return commission.value in commissions_values
