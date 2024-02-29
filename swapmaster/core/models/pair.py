from dataclasses import dataclass
from typing import Optional, TypeAlias

from .course import CourseId
from .method import MethodId
from .currency import Currency
from .commission import CommissionId

PairId: TypeAlias = int


@dataclass(slots=True)
class Pair:
    id: Optional[PairId]
    method_from: MethodId
    method_to: MethodId
    commission: CommissionId
    course_id: CourseId


@dataclass
class PairCurrencies:
    id: PairId
    currency_from: Currency
    currency_to: Currency
