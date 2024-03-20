from typing import Dict

from swapmaster.application.common.db.requisite_gateway import (
    RequisiteReader,
    RequisiteUpdater,
    RequisiteWriter
)
from swapmaster.core.models import RequisiteId, Requisite, PairId


class RequisiteGatewayMock(RequisiteReader, RequisiteUpdater, RequisiteWriter):
    def __init__(self):
        self.requisites: Dict[RequisiteId, Requisite] = {}

    async def add_requisite(self, requisite: Requisite) -> Requisite:
        max_of_ids = max(self.requisites) if self.requisites else 0
        new_requisite_id = max_of_ids + 1
        requisite.id = new_requisite_id
        self.requisites[requisite.id] = requisite
        return self.requisites[requisite.id]

    async def is_requisite_exists(self, requisite_name: str) -> bool:
        return requisite_name in [requisite.name for requisite in self.requisites.values()]

    async def get_requisites_of_pair(self, pair_id: PairId) -> list[Requisite]:
        requisites_of_pair = []
        for requisite in self.requisites.values():
            if requisite.pair_id == pair_id:
                requisites_of_pair.append(requisite)
        return requisites_of_pair

    async def get_requisite(self, requisite_id: RequisiteId) -> Requisite:
        return self.requisites[requisite_id]
