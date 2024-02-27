from dataclasses import dataclass

from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.db.requisite_gateway import RequisiteWriter
from swapmaster.application.common.uow import UoW
from swapmaster.core.models import Requisite, PairId
from swapmaster.core.services.requisite import RequisiteService


@dataclass
class NewRequisiteDTO:
    name: str
    pair_id: PairId
    regular_expression: str


class AddRequisite(Interactor[NewRequisiteDTO, Requisite]):
    def __init__(
            self,
            requisite_gateway: RequisiteWriter,
            uow: UoW,
            requisite_service: RequisiteService
    ):
        self.requisite_gateway = requisite_gateway
        self.uow = uow
        self.requisite_service = requisite_service

    async def __call__(self, data: NewRequisiteDTO) -> Requisite:
        new_requisite = self.requisite_service.create_requisite(
            name=data.name,
            pair_id=data.pair_id,
            regular_expression=data.regular_expression
        )
        saved_requisite = await self.requisite_gateway.add_requisite(requisite=new_requisite)
        await self.uow.commit()
        return saved_requisite
