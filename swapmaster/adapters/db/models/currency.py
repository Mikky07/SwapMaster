from sqlalchemy.orm import Mapped, mapped_column

from swapmaster.core.models import dto
from .base import Base


class Currency(Base):
    __tablename__ = "currencies"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    def to_dto(self) -> dto.Currency:
        return dto.Currency(
            currency_id=self.id,
            name=self.name
        )

    def __repr__(self):
        return f"<Currency id={self.id} name={self.name}>"
