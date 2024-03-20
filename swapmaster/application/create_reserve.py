from dataclasses import dataclass
from typing import Optional

from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.db.reserve_gateway import ReserveWriter
from swapmaster.application.common.uow import UoW
from swapmaster.core.constants import ReserveUpdateMethodEnum
from swapmaster.core.models import WalletId
from swapmaster.core.models.reserve import Reserve


@dataclass
class NewReserveDTO:
    size: Optional[float]
    update_method: ReserveUpdateMethodEnum


class CreateReserve(Interactor):
    def __init__(
            self,
            uow: UoW,
            reserve_gateway: ReserveWriter,
    ):
        self.uow = uow
        self.reserve_gateway = reserve_gateway

    async def __call__(self, data: NewReserveDTO) -> Reserve:
        new_reserve = Reserve(
            id=None,
            size=data.size,
            update_method=data.update_method,
            wallet_id=None
        )
        saved_reserve = await self.reserve_gateway.save_reserve(reserve=new_reserve)
        await self.uow.commit()
        return saved_reserve
