from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDBGateway
from swapmaster.adapters.db import models


class CourseGateway(BaseDBGateway):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Course, session)


