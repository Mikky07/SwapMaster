from typing import Optional, TypeAlias
from dataclasses import dataclass

CurrencyId: TypeAlias = int


@dataclass(frozen=True, slots=True)
class Currency:
    id: Optional[CurrencyId]
    name: str
