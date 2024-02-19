from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from swapmaster.core.models import RequisiteId, Requisite, OrderId
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
        filters = [models.Requisite.id == requisite_id]
        is_requisite_available = await self.is_model_exists(filters)
        return is_requisite_available

    async def add_requisite(self, requisite: Requisite) -> Requisite:
        saved_requisite = await self.create_model(
            pair_id=requisite.pair_id,
            name=requisite.name,
            regular_expression=requisite.regular_expression
        )
        return saved_requisite.to_dto()

    async def get_requisites_of_order(self, order_id: OrderId) -> list[Requisite]:
        stmt = (
            select(models.Requisite)
            .join(models.Order, models.Requisite.pair_id == models.Order.pair_id)
            .where(models.Order.id == order_id)
        )
        requisites = await self.session.scalars(stmt)
        return [requisite.to_dto() for requisite in requisites.all()]