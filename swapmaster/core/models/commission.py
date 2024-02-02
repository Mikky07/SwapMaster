from dataclasses import dataclass
from typing import NewType, Optional

CommissionId = NewType("CommissionId", int)


@dataclass
class Commission:
    commission_id: Optional[CommissionId]
    value: float
