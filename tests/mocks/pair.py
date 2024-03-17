from typing import Dict

from swapmaster.application.common.db.pair_gateway import PairReader, PairWriter
from swapmaster.core.models import PairId, Pair, MethodId, CourseId, Course


NEW_PAIR_ID = PairId(1)


class PairGatewayMock(PairReader, PairWriter):
    def __init__(self):
        self.pairs: Dict[PairId, Pair] = {}

    async def get_pair(self, method_from_id: MethodId, method_to_id: MethodId) -> Pair:
        ...

    async def get_pair_by_id(self, pair_id: PairId) -> Pair | None:
        if pair_id not in self.pairs:
            return
        return self.pairs[pair_id]

    async def add_pair(self, pair: Pair) -> Pair:
        self.pairs[NEW_PAIR_ID] = pair
        pair.id = NEW_PAIR_ID
        return self.pairs[pair.id]

    async def get_pair_course(self, course_id: CourseId) -> Course:
        ...
