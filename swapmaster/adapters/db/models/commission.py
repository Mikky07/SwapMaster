from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from swapmaster.core import models as dto


class Commission(Base):
    __tablename__ = "commissions"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[float]

    def __repr__(self):
        return f"<Commission id={self.id} value={self.value}>"

    def to_dto(self) -> dto.Commission:
        return dto.Commission(
            id=self.id,
            value=self.value
        )
