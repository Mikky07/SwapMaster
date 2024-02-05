from typing import TypeAlias
from dataclasses import dataclass

from swapmaster.core.models import PairId


CourseId: TypeAlias = int


@dataclass
class Course:
    course_id: CourseId
    pair_id: PairId
    value: float
