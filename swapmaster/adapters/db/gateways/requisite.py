from sqlalchemy.ext.asyncio import AsyncSession

from swapmaster.core.models import RequisiteId, Requisite
from .base import BaseDBGateway
from swapmaster.adapters.db import models
from swapmaster.application.common.protocols.requisite_gateway import (
    RequisiteReader,
    RequisiteUpdater,
    RequisiteWriter
)


class RequisiteGateway(
    BaseDBGateway[models.Requisite],
    RequisiteReader,
    RequisiteUpdater,
    RequisiteWriter
):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Requisite, session)

    async def get_requisite(self, requisite_id: RequisiteId) -> Requisite:
        requisite = await self.read_model(filters=[models.Requisite.id == requisite_id])
        return requisite.to_dto()

    async def is_requisite_available(self, requisite_id: RequisiteId) -> bool:
        requisite = await self.get_requisite(requisite_id)
        return requisite is not None

    async def add_requisite(self, requisite: Requisite) -> Requisite:
        saved_requisite = await self.create_model(
            pair_id=requisite.pair_id,
            name=requisite.name,
            regular_expression=requisite.regular_expression
        )
        return saved_requisite.to_dto()
