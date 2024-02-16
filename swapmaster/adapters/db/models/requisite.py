from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import Base
from swapmaster.core import models as dto


class Requisite(Base):
    __tablename__ = "requisites"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    regular_expression: Mapped[Optional[str]]

    pair_id = mapped_column(ForeignKey("pairs.id"))
    pair: Mapped["Pair"] = relationship(back_populates="requisites")

    def __repr__(self):
        return (
            f"<Requisite id={self.id}"
            f" name={self.name}"
            f" regular_expression={self.regular_expression}"
            f" pair_id={self.pair_id}>"
        )

    def to_dto(self) -> dto.Requisite:
        return dto.Requisite(
            requisite_id=self.id,
            name=self.name,
            regular_expression=self.regular_expression,
            pair_id=self.pair_id
        )

