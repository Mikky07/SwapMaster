from typing import Dict

from swapmaster.application.common.gateways.requisite_gateway import (
    RequisiteReader,
    RequisiteUpdater,
    RequisiteWriter
)
from swapmaster.core.models import RequisiteId, Requisite, PairId
from swapmaster.core.services.requisite import RequisiteService


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


class RequisiteServiceMock(RequisiteService):
    """We can transfer values that BL functions will return to check all cases simply"""
    def __init__(self):
        self.requisites_valid: bool = True

    def check_requisites_validity(self, *args, **kwargs) -> bool:
        return self.requisites_valid
