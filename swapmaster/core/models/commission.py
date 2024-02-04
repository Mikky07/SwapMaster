from dataclasses import dataclass
from typing import Optional, TypeAlias

CommissionId: TypeAlias = int


@dataclass
class Commission:
    commission_id: Optional[CommissionId]
    value: float
