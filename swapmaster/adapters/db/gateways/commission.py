import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.exc import InternalError, NoResultFound

from swapmaster.application.common.protocols.commission_gateway import (
    CommissionWriter,
    CommissionReader
)
from swapmaster.core.models import Commission, CommissionId
from swapmaster.adapters.db import models

logger = logging.getLogger(__name__)


class CommissionGateway(CommissionWriter, CommissionReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_commission(self, commission: Commission) -> Commission:
        kwargs = dict(value=commission.value)
        stmt = insert(models.Commission).values(**kwargs).returning(models.Commission)
        saved_commission = await self.session.execute(stmt)
        if not (result := saved_commission.scalar_one()):
            raise InternalError
        return Commission(
            commission_id=result.id,
            value=result.value
        )

    async def _get_by_id(self, _id: CommissionId):
        stmt = (
            select(models.Commission)
            .where(models.commission.Commission.id == _id)
        )
        result = await self.session.scalar(stmt)
        return result

    async def get_commission(self, commission_id: CommissionId) -> Commission:
        commission = await self._get_by_id(_id=commission_id)
        if not commission:
            raise NoResultFound
        return commission

    async def is_commission_available(self, value: float) -> bool:
        commission = await self.session.scalar(
            select(models.Commission).where(models.Commission.value == value)
        )
        return commission is None
