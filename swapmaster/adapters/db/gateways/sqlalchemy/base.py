from typing import TypeVar, Sequence, Generic

from sqlalchemy import select, insert, update, ScalarResult
from sqlalchemy.exc import NoResultFound
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.roles import ExpressionElementRole

from swapmaster.adapters.db.models import Base
from swapmaster.core.utils.exceptions import SMError

Model = TypeVar("Model", bound=Base)


class BaseDBGateway(Generic[Model]):
    def __init__(self, model: type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def is_model_exists(
            self,
            filters: Sequence[ExpressionElementRole] | None = None
    ) -> bool:
        stmt = select(func.count(self.model.id)).filter(*filters)
        model = await self.session.scalars(stmt)
        return model.one() > 0

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
        model_read = await self.__read_model_with_filters(filters=filters)
        if not (result := model_read.first()):
            raise NoResultFound
        return result

    async def __read_model_with_filters(
            self,
            filters: Sequence[ExpressionElementRole] | None = None
    ) -> ScalarResult[Model]:
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
    ) -> Model:
        stmt = update(self.model).values(kwargs).returning(self.model)
        if filters:
            stmt = stmt.filter(*filters)
        updated_model = await self.session.execute(stmt)
        if not (result := updated_model.scalar_one()):
            raise SMError(f"Some troubles with updating of {self.model.__name__} occurred")
        return result
