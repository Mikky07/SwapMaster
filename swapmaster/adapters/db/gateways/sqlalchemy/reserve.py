import logging

from sqlalchemy.ext.asyncio import AsyncSession

from swapmaster.core.constants import ReserveUpdateMethodEnum
from swapmaster.core.models import MethodId
from .base import BaseDBGateway
from swapmaster.adapters.db import models
from swapmaster.application.common.gateways.reserve_gateway import (
    ReserveWriter,
    ReserveUpdater,
    ReserveReader
)
from swapmaster.core.models.reserve import Reserve, ReserveId
from swapmaster.core.models.wallet import WalletId
from swapmaster.adapters.db.exceptions import exception_mapper

logger = logging.getLogger(__name__)


class ReserveGateway(
    BaseDBGateway[models.Reserve],
    ReserveWriter,
    ReserveUpdater,
    ReserveReader
):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Reserve, session)

    @exception_mapper
    async def attach_wallet(self, wallet_id: WalletId, reserve_id: ReserveId) -> Reserve:
        updated_reserve = await self.update_model(
            wallet_id=wallet_id,
            filters=[models.Reserve.id == reserve_id]
        )
        return updated_reserve.to_dto()

    @exception_mapper
    async def save_reserve(self, reserve: Reserve) -> Reserve:
        saved_reserve = await self.update_model(
            size=reserve.size,
            update_method=reserve.update_method
        )
        return saved_reserve.to_dto()

    @exception_mapper
    async def get_all_remote_reserves(self) -> list[Reserve]:
        remote_reserves = await self.get_model_list(
            [
                models.Reserve.update_method == ReserveUpdateMethodEnum.REMOTE
            ]
        )
        return [reserve.to_dto() for reserve in remote_reserves]

    @exception_mapper
    async def get_reserve_by_id(self, reserve_id: ReserveId) -> Reserve:
        reserve = await self.read_model([models.Reserve.id == reserve_id])
        return reserve.to_dto()

    @exception_mapper
    async def update_reserve_size(self, reserve_id: ReserveId, size: float) -> Reserve:
        updated_reserve = await self.update_model(
            size=size,
            filters=[models.Reserve.id == reserve_id]
        )
        return updated_reserve

    @exception_mapper
    async def get_reserve_of_method(self, method_id: MethodId) -> Reserve:
        reserve = await self.read_model([models.Reserve.method_id == method_id])
        return reserve.to_dto()
