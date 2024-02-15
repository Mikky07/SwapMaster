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
            filters: Sequence[ORMOption] | None = None
    ) -> Sequence[Model]:
        result = await self.__read_model_with_options(filters=filters)
        return result.all()

    async def read_model(
            self,
            filters: Sequence[ORMOption] | None = None
    ) -> Model:
        result = await self.__read_model_with_options(filters=filters)
        return result.first()

    async def __read_model_with_options(
            self,
            filters: Sequence[ORMOption] | None = None
    ):
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter(*filters)
        return await self.session.scalars(stmt)

    async def create_model(
            self,
            kwargs: dict
    ) -> Model:
        stmt = insert(self.model).values(kwargs).returning(self.model)
        saved_model = await self.session.execute(stmt)
        if not (result := saved_model.scalar_one()):
            raise SMError(f"Some troubles with insert of {self.model.__name__} occurred")
        return result

    async def update_model(
            self,
            kwargs: dict
    ):
        stmt = update(self.model).values(kwargs).returning(self.model)
        updated_model = await self.session.execute(stmt)
        if not (result := updated_model.scalar_one()):
            raise SMError(f"Some troubles with update of {self.model.__name__} occurred")
        return result
