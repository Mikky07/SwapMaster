from dataclasses import dataclass

from swapmaster.application.common.gateways import PairReader
from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.gateways.requisite_gateway import RequisiteWriter, RequisiteReader
from swapmaster.application.common.uow import UoW
from swapmaster.core.models import Requisite, PairId
from swapmaster.core.utils.exceptions import RequisiteAlreadyExists, PairNotExists


@dataclass
class NewRequisiteDTO:
    name: str
    pair_id: PairId
    regular_expression: str


class CreateRequisite(Interactor[NewRequisiteDTO, Requisite]):
    def __init__(
            self,
            requisite_gateway: RequisiteWriter | RequisiteReader,
            pair_gateway: PairReader,
            uow: UoW
    ):
        self.requisite_gateway = requisite_gateway
        self.pair_gateway = pair_gateway
        self.uow = uow

    async def __call__(self, data: NewRequisiteDTO) -> Requisite:
        new_requisite = Requisite(
            id=None,
            name=data.name,
            pair_id=data.pair_id,
            regular_expression=data.regular_expression
        )
        is_requisite_exists = await self.requisite_gateway.is_requisite_exists(data.name)
        if is_requisite_exists:
            raise RequisiteAlreadyExists("Requisite with this name already exists!")
        is_pair_exists = await self.pair_gateway.get_pair_by_id(pair_id=data.pair_id)
        if not is_pair_exists:
            raise PairNotExists("Can't find pair with this ID!")
        saved_requisite = await self.requisite_gateway.add_requisite(requisite=new_requisite)
        await self.uow.commit()
        return saved_requisite
