from sqlalchemy.ext.asyncio import AsyncSession

from swapmaster.core.models import dto
from swapmaster.adapters.db import models
from swapmaster.application.common.currency_gateway import CurrencyListReader


class CurrencyGateway(CurrencyListReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_currency_list(self) -> list[dto.Currency]:
        currency_id = dto.CurrencyId(123)
        return [dto.Currency(currency_id, "Test currency")]
