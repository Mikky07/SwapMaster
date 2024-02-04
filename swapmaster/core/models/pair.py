from dataclasses import dataclass
from typing import Optional, TypeAlias

from .method import MethodId
from .commission import CommissionId


PairId: TypeAlias = int


@dataclass
class Pair:
    pair_id: Optional[PairId]
    method_from: MethodId
    method_to: MethodId
    commission: CommissionId
