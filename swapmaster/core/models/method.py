from dataclasses import dataclass
from typing import Optional, TypeAlias

from swapmaster.core.models.currency import CurrencyId
from swapmaster.core.models.reserve import ReserveId

MethodId: TypeAlias = int


@dataclass
class Method:
    method_id: Optional[MethodId]
    reserve: ReserveId
    currency_id: CurrencyId
    name: str
