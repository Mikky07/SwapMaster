import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .base import BaseGateway
from swapmaster.adapters.db import models
from swapmaster.application.common.protocols.reserve_gateway import (
    ReserveWriter,
    ReserveUpdater,
    ReserveReader
)
from swapmaster.application.common.protocols.reserve_size_obtainer import RemoteReserve
from swapmaster.core.models.reserve import Reserve, ReserveId
from swapmaster.core.models.wallet import WalletId


logger = logging.getLogger(__name__)


class ReserveGateway(BaseGateway[models.Reserve], ReserveWriter, ReserveUpdater, ReserveReader):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Reserve, session)

    async def is_reserve_available(self, reserve_id) -> ReserveId:
        ...

    async def attach_wallet(self, wallet_id: WalletId, reserve_id: ReserveId) -> Reserve:
        updated_reserve = await self.update_model(
            wallet_id=wallet_id,
            filters=[models.Reserve.id == reserve_id]
        )
        return updated_reserve.to_dto()

    async def add_reserve(self, reserve: Reserve) -> Reserve:
        saved_reserve = await self.update_model(
            size=reserve.size,
            update_method=reserve.update_method
        )
        return saved_reserve.to_dto()

    async def get_all_remote_reserves(self) -> list[RemoteReserve]:
        stmt = (
            select(models.Reserve.id, models.Wallet.address)
            .join(models.Reserve.wallet)
        )
        result = await self.session.execute(stmt)
        return [
            RemoteReserve(
                reserve_id=remote_reserve.id,
                wallet_address=remote_reserve.address
            )
            for remote_reserve in result.all()
        ]

    async def update_reserve_size(self, reserve_id: ReserveId, size: float) -> Reserve:
        updated_reserve = await self.update_model(
            size=size,
            filters=[models.Reserve.id == reserve_id]
        )
        return updated_reserve
