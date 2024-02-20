from typing import Optional, TypeAlias

from dataclasses import dataclass

from swapmaster.core.models.wallet import WalletId
from swapmaster.core.constants import ReserveUpdateMethodEnum

ReserveId: TypeAlias = int


@dataclass
class Reserve:
    id: Optional[ReserveId]
    size: float
    update_method: ReserveUpdateMethodEnum
    wallet_id: Optional[WalletId]
