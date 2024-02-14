import logging

from sqlalchemy.exc import InternalError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select

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


class ReserveGateway(ReserveWriter, ReserveUpdater, ReserveReader):
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

    async def update_reserve_size(self, reserve_id: ReserveId, size: float) -> None:
        logger.info("Reserve with id: %s and size %s is updating", reserve_id, size)
        kwargs = dict(size=size)
        stmt = (
            update(models.Reserve)
            .values(kwargs)
            .where(models.Reserve.id == reserve_id)
            .returning(models.Reserve)
        )
        updated_reserve = await self.session.execute(stmt)
        if not updated_reserve.scalar_one():
            raise InternalError
