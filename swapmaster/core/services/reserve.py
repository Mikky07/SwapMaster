from typing import Optional

from swapmaster.core.models.wallet import WalletId
from swapmaster.core.models.reserve import Reserve
from swapmaster.core.models.method import MethodId
from swapmaster.core.constants import ReserveUpdateMethodEnum


class ReserveService:
    def create_reserve(
            self,
            method_id: MethodId,
            initial_size: float,
            update_method: ReserveUpdateMethodEnum,
            wallet: Optional[WalletId] = None
    ) -> Reserve:
        return Reserve(
            reserve_id=None,
            method_id=method_id,
            size=initial_size,
            update_method=update_method,
            wallet_id=wallet
        )
