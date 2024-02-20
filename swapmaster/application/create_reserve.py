from dataclasses import dataclass
from typing import Optional

from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.protocols.reserve_gateway import ReserveWriter
from swapmaster.application.common.uow import UoW
from swapmaster.core.constants import ReserveUpdateMethodEnum
from swapmaster.core.models.reserve import Reserve
from swapmaster.core.services.reserve import ReserveService


@dataclass
class NewReserveDTO:
    size: Optional[float]
    update_method: ReserveUpdateMethodEnum


class AddReserve(Interactor):
    def __init__(
            self,
            uow: UoW,
            reserve_gateway: ReserveWriter,
            reserve_service: ReserveService,
    ):
        self.uow = uow
        self.reserve_gateway = reserve_gateway
        self.reserve_service = reserve_service

    async def __call__(self, data: NewReserveDTO) -> Reserve:
        new_reserve = self.reserve_service.create_reserve(
            initial_size=data.size,
            update_method=data.update_method
        )
        saved_reserve = await self.reserve_gateway.add_reserve(reserve=new_reserve)
        await self.uow.commit()
        return saved_reserve
