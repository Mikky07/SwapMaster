import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from swapmaster.adapters.db.models import Base
from swapmaster.core import models as dto

if typing.TYPE_CHECKING:
    from swapmaster.adapters.db.models import Method


class Currency(Base):
    __tablename__ = "currencies"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)

    method: Mapped[list['Method']] = relationship(
        back_populates="currency",
        foreign_keys="Method.currency_id"
    )

    def __repr__(self):
        return f"<Currency id={self.id} name={self.name}>"

    def to_dto(self) -> dto.Currency:
        return dto.Currency(
            id=self.id,
            name=self.name
        )
