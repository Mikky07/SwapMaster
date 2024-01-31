from typing import NewType
from dataclasses import dataclass

CurrencyId = NewType("CurrencyId", int)


@dataclass(frozen=True)
class Currency:
    currency_id: CurrencyId
    name: str
