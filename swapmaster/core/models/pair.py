from dataclasses import dataclass
from typing import NewType, Optional

from .method import MethodId
from .commission import CommissionId


PairId = NewType("PairId", int)


@dataclass
class Pair:
    pair_id: Optional[PairId]
    method_from: MethodId
    method_to: MethodId
    commission: Optional[CommissionId]
