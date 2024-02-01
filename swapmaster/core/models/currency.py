from typing import NewType, Optional
from dataclasses import dataclass

CurrencyId = NewType("CurrencyId", int)


@dataclass(frozen=True)
class Currency:
    currency_id: Optional[CurrencyId]
    name: str
