import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from swapmaster.adapters.db.gateways.base import BaseGateway
from swapmaster.application.common.protocols.pair_gateway import PairReader, PairWriter
from swapmaster.core.models import Pair, PairId
from swapmaster.adapters.db import models
from swapmaster.core.models.pair import PairCurrencies

logger = logging.getLogger(__name__)


class PairGateway(BaseGateway[models.Pair], PairReader, PairWriter):

    def __init__(self, session: AsyncSession):
        super().__init__(models.Pair, session)

    async def get_pair(self, pair_id: PairId) -> Pair:
        pair = await self.read_model(filters=[models.Pair.id == pair_id])
        return pair.to_dto()

    async def get_pair_currencies(self, pair_id: PairId) -> PairCurrencies:
        currency_from = await self.session.scalar(
            select(models.Currency)
            .join(models.Pair.method_from)
            .where(models.Pair.id == pair_id)
            .where(models.Currency.id == models.Method.currency_id)
        )
        currency_to = await self.session.scalar(
            select(models.Currency)
            .join(models.Pair.method_to)
            .where(models.Pair.id == pair_id)
            .where(models.Currency.id == models.Method.currency_id)
        )
        if not currency_to and currency_from:
            raise NoResultFound
        return PairCurrencies(
            currency_from=currency_from.to_dto(),
            currency_to=currency_to.to_dto(),
            pair_id=pair_id
        )

    async def add_pair(self, pair: Pair) -> Pair:
        saved_pair = await self.create_model(
            method_to_id=pair.method_to,
            method_from_id=pair.method_from,
            commission_id=pair.commission
        )
        return saved_pair.to_dto()
