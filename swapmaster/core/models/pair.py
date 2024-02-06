from dataclasses import dataclass
from typing import Optional, TypeAlias

from .method import MethodId
from .currency import Currency
from .commission import CommissionId
from ..constants import CourseObtainingMethod

PairId: TypeAlias = int


@dataclass
class Pair:
    pair_id: Optional[PairId]
    method_from: MethodId
    method_to: MethodId
    commission: CommissionId


@dataclass
class PairCurrencies:
    pair_id: PairId
    currency_from: Currency
    currency_to: Currency
