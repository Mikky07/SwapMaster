from typing import Protocol
from abc import abstractmethod

from swapmaster.core.models import PairId, Pair, MethodId, Course, CourseId


class PairReader(Protocol):
    @abstractmethod
    async def get_pair(self, method_from_id: MethodId, method_to_id: MethodId) -> Pair:
        raise NotImplementedError

    @abstractmethod
    async def get_pair_by_id(self, pair_id: PairId) -> Pair:
        raise NotImplementedError

    @abstractmethod
    async def obtain_course(self, course_id: CourseId) -> Course:
        raise NotImplementedError


class PairWriter(Protocol):
    @abstractmethod
    async def add_pair(self, pair: Pair) -> Pair:
        raise NotImplementedError
