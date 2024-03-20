from dataclasses import dataclass

from swapmaster.application.common.uow import UoW
from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.db.pair_gateway import PairWriter
from swapmaster.core.models import Pair, MethodId, CommissionId, CourseId, WalletId


@dataclass
class NewPairDTO:
    method_from: MethodId
    method_to: MethodId
    commission: CommissionId
    course_id: CourseId
    wallet_id: WalletId


class CreatePair(Interactor):
    def __init__(self, pair_gateway: PairWriter, uow: UoW):
        self.pair_gateway = pair_gateway
        self.uow = uow

    async def __call__(self, data: NewPairDTO) -> Pair:
        new_pair = Pair(
            id=None,
            method_from=data.method_from,
            method_to=data.method_to,
            commission=data.commission,
            course_id=data.course_id,
            reception_wallet=data.wallet_id
        )
        saved_pair = await self.pair_gateway.add_pair(pair=new_pair)
        await self.uow.commit()
        return saved_pair
