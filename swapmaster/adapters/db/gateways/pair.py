import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from swapmaster.application.common.protocols.pair_gateway import PairReader
from swapmaster.core.models import Pair, PairId
from swapmaster.adapters.db import models
from swapmaster.core.models.pair import PairCurrencies

logger = logging.getLogger(__name__)


class PairGateway(PairReader):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_pair(self, pair_id: PairId) -> Pair:
        stmt = select(models.Pair).where(models.Pair.id == pair_id)
        result: models.Pair = await self.session.scalar(stmt)
        if not result:
            raise NoResultFound
        return Pair(
            pair_id=result.id,
            method_from=result.method_from_id,
            method_to=result.method_to_id,
            commission=result.commission_id,
            course_obtaining_method=result.course_obtaining_method
        )

    async def get_pair_currencies(self, pair_id: PairId) -> PairCurrencies:
        currency_from = await self.session.scalar(
            select(models.Currency)
            .join(models.Pair.method_from)
            .where(models.Pair.id == pair_id)
        )
        currency_to = await self.session.scalar(
            select(models.Currency)
            .join(models.Pair.method_to)
            .where(models.Pair.id == pair_id)
        )
        logger.info(currency_to)
        logger.info(currency_from)
        if not currency_to and currency_from:
            raise NoResultFound
        return PairCurrencies(
            currency_from=currency_from,
            currency_to=currency_to,
            pair_id=pair_id
        )
