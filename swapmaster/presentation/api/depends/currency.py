from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from swapmaster.adapters.db.currency_db import CurrencyGateway


class CurrencyDBProvider:
    def __init__(self, pool: async_sessionmaker[AsyncSession]):
        self.pool = pool

    async def get_currency_db(self) -> CurrencyGateway:
        async with self.pool() as session:
            yield CurrencyGateway(session)
