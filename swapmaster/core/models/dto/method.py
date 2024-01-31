from dataclasses import dataclass
from typing import NewType

from swapmaster.core.models.dto.currency import CurrencyId

MethodId = NewType("MethodId", int)


@dataclass
class Method:
    method_id: MethodId
    currency_id: CurrencyId
    method_name: str
