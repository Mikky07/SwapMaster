from dataclasses import dataclass
from typing import TypeAlias


WalletId: TypeAlias = int


@dataclass(slots=True)
class Wallet:
    id: WalletId
    name: str
    blockchain: str
    address: str
