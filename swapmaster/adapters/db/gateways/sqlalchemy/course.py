import logging

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDBGateway
from swapmaster.adapters.db import models
from swapmaster.application.common.gateways.course_gateway import CourseReader, CourseUpdater
from swapmaster.core.models import Course, CourseId

logger = logging.getLogger(__name__)


class CourseGateway(
    BaseDBGateway[models.Course],
    CourseReader,
    CourseUpdater
):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Method, session)

    async def update_course_value(self, value: float) -> Course:
        ...

    async def get_course_by_id(self, course_id: CourseId) -> Course:
        ...
