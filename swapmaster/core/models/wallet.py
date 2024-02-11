from dataclasses import dataclass
from typing import TypeAlias

from swapmaster.core.models.reserve import ReserveId


WalletId: TypeAlias = int


@dataclass
class Wallet:
    wallet_id: WalletId
    reserve_id: ReserveId
    link: str
