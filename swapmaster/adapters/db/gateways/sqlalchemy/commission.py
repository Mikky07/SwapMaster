import logging

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDBGateway
from swapmaster.application.common.db import (
    CommissionWriter,
    CommissionReader
)
from swapmaster.core.models import Commission, CommissionId
from swapmaster.adapters.db import models

logger = logging.getLogger(__name__)


class CommissionGateway(BaseDBGateway, CommissionWriter, CommissionReader):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Commission, session)

    async def add_commission(self, commission: Commission) -> Commission:
        saved_commission = await self.create_model(value=commission.value)
        return saved_commission.to_dto()

    async def get_commission(self, commission_id: CommissionId) -> Commission:
        commission = await self.read_model([models.Commission.id == commission_id])
        return commission.to_dto()

    async def is_commission_available(self, value: float) -> bool:
        commission = await self.read_model([models.Commission.value == value])
        return commission is None