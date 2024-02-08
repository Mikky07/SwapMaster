from dataclasses import dataclass

from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.protocols.pair_gateway import PairWriter
from swapmaster.core.models import Pair, MethodId, CommissionId
from swapmaster.core.services.pair import PairService


@dataclass
class NewPairDTO:
    method_from: MethodId
    method_to: MethodId
    commission: CommissionId


class AddPair(Interactor[NewPairDTO, Pair]):
    def __init__(self, pair_gateway: PairWriter, pair_service: PairService):
        self.pair_gateway = pair_gateway
        self.pair_service = pair_service

    async def __call__(self, data: NewPairDTO) -> Pair:
        new_pair = self.pair_service.create_pair(
            method_from=data.method_from,
            method_to=data.method_to,
            commission=data.commission
        )
        saved_pair = await self.pair_gateway.add_pair(pair=new_pair)
        return saved_pair
