from sqlalchemy.exc import InternalError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update

from swapmaster.adapters.db import models
from swapmaster.application.common.protocols.reserve_gateway import ReserveWriter, ReserveUpdater
from swapmaster.core.models.reserve import Reserve, ReserveId
from swapmaster.core.models.wallet import WalletId


class ReserveGateway(ReserveWriter, ReserveUpdater):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_reserve_available(self, reserve_id) -> ReserveId:
        ...

    async def attach_wallet(self, wallet_id: WalletId, reserve_id: ReserveId) -> Reserve:
        kwargs = dict(wallet_id=wallet_id)
        stmt = (
            update(models.Reserve)
            .values(kwargs)
            .where(models.Reserve.id == reserve_id)
            .returning(models.Reserve)
        )
        updated_reserve = await self.session.execute(stmt)
        return updated_reserve.scalar_one().to_dto()

    async def add_reserve(self, reserve: Reserve) -> Reserve:
        kwargs = dict(
            size=reserve.size,
            method_id=reserve.method_id,
            update_method=reserve.update_method
        )
        stmt = (
            insert(models.Reserve)
            .values(kwargs)
            .returning(models.Reserve)
        )
        new_reserve = await self.session.execute(stmt)
        if not (result := new_reserve.scalar_one()):
            raise InternalError
        return result.to_dto()
