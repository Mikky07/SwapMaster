from typing import Generic, TypeVar, Sequence

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from swapmaster.adapters.db.models import Base
from swapmaster.core.utils.exceptions import SMError

Model = TypeVar("Model", bound=Base)


class BaseGateway(Generic[Model]):
    def __init__(self, model: type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_model_list(
            self,
            options: Sequence[ORMOption] | None = None
    ):
        result = await self._read_model_with_options(options=options)
        return result.all()

    async def read_model(
            self,
            options: Sequence[ORMOption] | None = None
    ):
        result = await self._read_model_with_options(options=options)
        return result.first()

    async def _read_model_with_options(
            self,
            options: Sequence[ORMOption] | None = None
    ):
        stmt = select(self.model)
        if options:
            stmt.options = options
        return await self.session.scalars(stmt)

    async def create_model(
            self,
            kwargs: dict
    ) -> Model:
        stmt = insert(self.model).values(kwargs).returning(self.model)
        saved_model = await self.session.execute(stmt)
        if not (result := saved_model.scalar_one()):
            raise SMError("Some troubles with insert occurred")
        return result

    async def update_model(
            self,
            kwargs: dict
    ):
        stmt = update(self.model).values(kwargs).returning(self.model)
        updated_model = await self.session.execute(stmt)
        if not (result := updated_model.scalar_one()):
            raise SMError("Some troubles with insert occurred")
        return result
