from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import Base


class Method(Base):
    __tablename__ = "methods"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)

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

    def __repr__(self):
        return f"<Method id={self.id} name={self.name} currency_id={self.currency_id}>"