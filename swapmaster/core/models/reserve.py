from typing import Optional, TypeAlias

from dataclasses import dataclass

from swapmaster.core.models.wallet import WalletId
from swapmaster.core.constants import ReserveUpdateMethodEnum
from swapmaster.core.models import MethodId

ReserveId: TypeAlias = int


@dataclass
class Reserve:
    reserve_id: Optional[ReserveId]
    method_id: MethodId
    size: float
    update_method: ReserveUpdateMethodEnum
    wallet_id: Optional[WalletId]
