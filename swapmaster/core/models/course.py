from dataclasses import dataclass
from typing import TypeAlias, Optional

from swapmaster.core.constants import CourseUpdateMethodEnum


CourseId: TypeAlias = int


@dataclass(slots=True)
class Course:
    id: Optional[CourseId]
    value: float
    update_method: CourseUpdateMethodEnum
