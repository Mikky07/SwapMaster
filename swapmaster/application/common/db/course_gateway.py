from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import PairId, Course


class CourseReader(Protocol):
    @abstractmethod
    async def get_course(self, pair_id: PairId) -> Course:
        raise NotImplementedError
