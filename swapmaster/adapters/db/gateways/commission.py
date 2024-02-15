import logging

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseGateway
from swapmaster.application.common.protocols.commission_gateway import (
    CommissionWriter,
    CommissionReader
)
from swapmaster.core.models import Commission, CommissionId
from swapmaster.adapters.db import models

logger = logging.getLogger(__name__)


class CommissionGateway(BaseGateway[models.Commission], CommissionWriter, CommissionReader):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Commission, session)

    async def add_commission(self, commission: Commission) -> Commission:
        kwargs = dict(value=commission.value)
        result = await self.create_model(kwargs=kwargs)
        return Commission(
            commission_id=result.id,
            value=result.value
        )

    async def get_commission(self, commission_id: CommissionId) -> Commission:
        commission = await self.read_model([models.Commission.id == commission_id])
        return Commission(
            commission_id=commission.id,
            value=commission.value
        )

    async def is_commission_available(self, value: float) -> bool:
        commission = await self.read_model([models.Commission.value == value])
        return commission is None
