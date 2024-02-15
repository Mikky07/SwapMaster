import logging

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseGateway
from swapmaster.adapters.db import models
from swapmaster.core.models import Currency
from swapmaster.application.common.protocols.currency_gateway import CurrencyListReader


logger = logging.getLogger(__name__)


class CurrencyGateway(BaseGateway[models.Currency], CurrencyListReader):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Currency, session)

    async def get_currency_list(self) -> list[Currency]:
        currencies = await self.get_model_list()
        return [
            Currency(
                currency_id=currency.id,
                name=currency.name
            ) for currency in currencies
        ]
