import logging

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDBGateway
from swapmaster.adapters.db import models
from swapmaster.core.models import Currency
from swapmaster.application.common.db.currency_gateway import CurrencyListReader
from swapmaster.adapters.db.exceptions import exception_mapper

logger = logging.getLogger(__name__)


class CurrencyGateway(BaseDBGateway, CurrencyListReader):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Currency, session)

    @exception_mapper
    async def get_currency_list(self) -> list[Currency]:
        currencies = await self.get_model_list()
        return [currency.to_dto() for currency in currencies]
