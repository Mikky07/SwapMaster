from typing import Dict

from swapmaster.core.models import Course, CourseId
from swapmaster.application.common.gateways.course_gateway import (
    CourseReader,
    CourseUpdater
)


class CourseGatewayMock(CourseReader, CourseUpdater):
    def __init__(self):
        self.courses: Dict[CourseId, Course] = {}

    async def get_course_by_id(self, course_id: CourseId) -> Course:
        return self.courses[course_id]

    async def update_course_value(self, value: float) -> Course:
        ...
