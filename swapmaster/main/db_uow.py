from sqlalchemy.ext.asyncio import AsyncSession

from swapmaster.application.common import UoW


class UowAsyncSession(UoW):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
