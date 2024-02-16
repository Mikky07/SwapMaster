from typing import Generic, TypeVar, Sequence

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.roles import ExpressionElementRole

from swapmaster.adapters.db.models import Base
from swapmaster.core.utils.exceptions import SMError

Model = TypeVar("Model", bound=Base)


class BaseGateway(Generic[Model]):
    def __init__(self, model: type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_model_list(
            self,
            filters: Sequence[ExpressionElementRole] | None = None
    ) -> Sequence[Model]:
        result = await self.__read_model_with_filters(
            filters=filters
        )
        return result.all()

    async def read_model(
            self,
            filters: Sequence[ExpressionElementRole] | None = None
    ) -> Model:
        result = await self.__read_model_with_filters(filters=filters)
        return result.first()

    async def __read_model_with_filters(
            self,
            filters: Sequence[ExpressionElementRole] | None = None
    ):
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter(*filters)
        return await self.session.scalars(stmt)

    async def create_model(
            self,
            **kwargs
    ) -> Model:
        stmt = insert(self.model).values(kwargs).returning(self.model)
        saved_model = await self.session.execute(stmt)
        if not (result := saved_model.scalar_one()):
            raise SMError(f"Some troubles with inserting of {self.model.__name__} occurred")
        return result

    async def update_model(
            self,
            filters: Sequence[ExpressionElementRole] | None = None,
            **kwargs
    ):
        stmt = update(self.model).values(kwargs).returning(self.model)
        if filters:
            stmt = stmt.filter(*filters)
        updated_model = await self.session.execute(stmt)
        if not (result := updated_model.scalar_one()):
            raise SMError(f"Some troubles with updating of {self.model.__name__} occurred")
        return result
