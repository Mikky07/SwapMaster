from dataclasses import dataclass
from typing import Optional, TypeAlias

from swapmaster.core.models.currency import CurrencyId

MethodId: TypeAlias = int


@dataclass
class Method:
    method_id: Optional[MethodId]
    currency_id: CurrencyId
    name: str
