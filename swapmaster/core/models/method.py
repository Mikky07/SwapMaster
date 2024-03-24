from dataclasses import dataclass
from typing import Optional, TypeAlias

from swapmaster.core.models.currency import CurrencyId
from swapmaster.core.models.reserve import ReserveId

MethodId: TypeAlias = int


@dataclass(slots=True)
class Method:
    id: Optional[MethodId]
    reserve_id: Optional[ReserveId]
    currency_id: CurrencyId
    name: str
