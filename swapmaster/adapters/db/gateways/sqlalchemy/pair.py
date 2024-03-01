import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from swapmaster.adapters.db.gateways.sqlalchemy.base import BaseDBGateway
from swapmaster.application.common.db.pair_gateway import PairReader, PairWriter
from swapmaster.core.models import Pair, PairId, MethodId, CourseId, Course
from swapmaster.adapters.db import models
from swapmaster.core.models.pair import PairCurrencies
from swapmaster.core.utils.exceptions import SMError

logger = logging.getLogger(__name__)


class PairGateway(BaseDBGateway, PairReader, PairWriter):

    def __init__(self, session: AsyncSession):
        super().__init__(models.Pair, session)

    async def get_pair(self, method_from_id: MethodId, method_to_id: MethodId) -> Pair:
        filters = [
            and_(
                 models.Pair.method_to_id == method_to_id,
                 models.Pair.method_from_id == method_from_id
            )
        ]
        is_pair_available = await self.is_model_exists(filters=filters)
        if not is_pair_available:
            raise SMError("That pair does not exists")
        pair = await self.read_model(
            filters=filters
        )
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
            id=pair_id,
            currency_from=currency_from.to_dto(),
            currency_to=currency_to.to_dto(),
        )

    async def add_pair(self, pair: Pair) -> Pair:
        saved_pair = await self.create_model(
            method_to_id=pair.method_to,
            method_from_id=pair.method_from,
            commission_id=pair.commission
        )
        return saved_pair.to_dto()

    async def get_pair_by_id(self, pair_id: PairId) -> Pair:
        pair = await self.read_model([models.Pair.id == pair_id])
        return pair.to_dto()

    async def obtain_course(self, course_id: CourseId) -> Course:
        stmt = select(models.Course).filter(models.Course.id == course_id)
        result = await self.session.scalars(stmt)
        if not (course := result.first()):
            raise SMError("Course not found")
        return course