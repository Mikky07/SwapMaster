from dataclasses import dataclass
from typing import TypeAlias

from swapmaster.core.constants import CourseUpdateMethodEnum


CourseId: TypeAlias = int


@dataclass
class Course:
    id: CourseId
    pair_id: 'PairId'
    value: float
    update_method: CourseUpdateMethodEnum
