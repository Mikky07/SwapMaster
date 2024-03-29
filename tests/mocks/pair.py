from typing import Dict

from swapmaster.application.common.gateways.pair_gateway import PairReader, PairWriter
from swapmaster.core.models import PairId, Pair, MethodId, CourseId, Course


class PairGatewayMock(PairReader, PairWriter):
    def __init__(self):
        self.pairs: Dict[PairId, Pair] = {}

    async def get_pair(self, method_from_id: MethodId, method_to_id: MethodId) -> Pair:
        for pair in self.pairs.values():
            if pair.method_to_id == method_to_id and pair.method_from_id == method_from_id:
                return pair

    async def get_pair_by_id(self, pair_id: PairId) -> Pair | None:
        if pair_id not in self.pairs:
            return
        return self.pairs[pair_id]

    async def add_pair(self, pair: Pair) -> Pair:
        max_of_ids = max(self.pairs) if self.pairs else 0
        new_pair_id = max_of_ids + 1
        pair.id = new_pair_id
        self.pairs[pair.id] = pair
        return self.pairs.get(pair.id)

    async def get_pair_course(self, course_id: CourseId) -> Course:
        ...
