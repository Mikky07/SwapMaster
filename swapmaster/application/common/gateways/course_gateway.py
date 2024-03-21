from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import Course, CourseId


class CourseReader(Protocol):
    @abstractmethod
    async def get_course_by_id(self, course_id: CourseId) -> Course:
        raise NotImplementedError


class CourseUpdater(Protocol):
    @abstractmethod
    async def update_course_value(self, value: float) -> Course:
        raise NotImplementedError
