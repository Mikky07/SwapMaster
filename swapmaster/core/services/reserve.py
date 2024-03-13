from typing import Optional

from swapmaster.core.models.wallet import WalletId
from swapmaster.core.models.reserve import Reserve
from swapmaster.core.constants import ReserveUpdateMethodEnum


class ReserveService:
    def create_reserve(
            self,
            initial_size: float,
            update_method: ReserveUpdateMethodEnum,
            wallet_id: Optional[WalletId] = None
    ) -> Reserve:
        return Reserve(
            id=None,
            size=initial_size,
            update_method=update_method,
            wallet_id=wallet_id
        )
