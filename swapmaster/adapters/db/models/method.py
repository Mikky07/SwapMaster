from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import Base


class Method(Base):
    __tablename__ = "methods"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    currency_id = mapped_column(
        ForeignKey(
            "currencies.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    currency: Mapped["Currency"] = relationship(
        back_populates="method",
        foreign_keys=currency_id,
    )

    reserve_id = mapped_column(ForeignKey("reserves.id"))
    reserve: Mapped[Optional['Reserve']] = relationship(back_populates="method")

    def __repr__(self):
        return (
            f"<Method id={self.id}"
            f" name={self.name} "
            f" currency_id={self.currency_id}"
            f" reserve_id={self.reserve_id}>"
        )
