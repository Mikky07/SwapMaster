from dataclasses import dataclass
from typing import NewType, Optional

from swapmaster.core.models.currency import CurrencyId

MethodId = NewType("MethodId", int)


@dataclass
class Method:
    method_id: Optional[MethodId]
    currency_id: CurrencyId
    name: str
