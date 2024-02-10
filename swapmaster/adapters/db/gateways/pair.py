import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.exc import NoResultFound, InternalError

from swapmaster.application.common.protocols.pair_gateway import PairReader, PairWriter
from swapmaster.core.models import Pair, PairId, Currency
from swapmaster.adapters.db import models
from swapmaster.core.models.pair import PairCurrencies

logger = logging.getLogger(__name__)


class PairGateway(PairReader, PairWriter):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_pair(self, pair_id: PairId) -> Pair:
        stmt = select(models.Pair).where(models.Pair.id == pair_id)
        result: Optional[models.Pair] = await self.session.scalar(stmt)
        if not result:
            raise NoResultFound
        return Pair(
            pair_id=result.id,
            method_from=result.method_from_id,
            method_to=result.method_to_id,
            commission=result.commission_id
        )

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
            currency_from=Currency(
                currency_id=currency_from.id,
                name=currency_from.name,
            ),
            currency_to=Currency(
                currency_id=currency_to.id,
                name=currency_to.name,
            ),
            pair_id=pair_id
        )

    async def add_pair(self, pair: Pair) -> Pair:
        logger.info(pair)
        kwargs = dict(
            method_to_id=pair.method_to,
            method_from_id=pair.method_from,
            commission_id=pair.commission
        )
        stmt = insert(models.Pair).values(kwargs).returning(models.Pair)
        saved_pair = await self.session.execute(stmt)
        if not (result := saved_pair.scalar_one()):
            raise InternalError
        return Pair(
            pair_id=result.id,
            method_to=result.method_to_id,
            method_from=result.method_from_id,
            commission=result.commission_id
        )
