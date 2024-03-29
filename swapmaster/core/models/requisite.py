from dataclasses import dataclass
from typing import TypeAlias, Optional

from swapmaster.core.models.pair import PairId

RequisiteId: TypeAlias = int


@dataclass(slots=True)
class Requisite:
    id: Optional[RequisiteId]
    pair_id: PairId
    name: str
    regular_expression: Optional[str]
