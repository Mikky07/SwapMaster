import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, ScalarResult

from swapmaster.adapters.db import models
from swapmaster.core.models import Currency
from swapmaster.application.common.protocols.currency_gateway import CurrencyListReader


logger = logging.getLogger(__name__)


class CurrencyGateway(CurrencyListReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_currency_list(self) -> list[Currency]:
        stmt = select(models.Currency)
        currencies: ScalarResult[models.Currency] = await self.session.scalars(stmt)
        return [
            Currency(
                currency_id=currency.id,
                name=currency.name
            ) for currency in currencies.all()
        ]
