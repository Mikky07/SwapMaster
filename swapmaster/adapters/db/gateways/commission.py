import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.exc import InternalError

from swapmaster.application.common.protocols.commission_gateway import CommissionWriter
from swapmaster.core.models import Commission
from swapmaster.adapters.db import models

logger = logging.getLogger(__name__)


class CommissionGateway(CommissionWriter):
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

    async def is_commission_available(self, value: float) -> bool:
        commission = await self.session.scalar(
            select(models.Commission).where(models.Commission.value == value)
        )
        return commission is None
