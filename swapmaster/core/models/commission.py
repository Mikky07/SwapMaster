from dataclasses import dataclass
from typing import Optional, TypeAlias

CommissionId: TypeAlias = int


@dataclass(slots=True)
class Commission:
    id: Optional[CommissionId]
    value: float
