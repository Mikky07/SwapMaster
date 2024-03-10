import typing
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship, mapped_column, Mapped

from swapmaster.core.constants import ReserveUpdateMethodEnum
from swapmaster.core import models as dto
from swapmaster.adapters.db.models import Base

if typing.TYPE_CHECKING:
    from swapmaster.adapters.db import models


class Reserve(Base):
    __tablename__ = "reserves"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    size: Mapped[float]
    update_method: Mapped[ReserveUpdateMethodEnum] = mapped_column(
        ENUM(ReserveUpdateMethodEnum)
    )

    method_id: Mapped[int]
    method = relationship("Method", back_populates="reserve", foreign_keys='Method.reserve_id')

    wallet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wallets.id"))
    wallet: Mapped[Optional[models.Wallet]] = relationship(back_populates="reserve", foreign_keys=wallet_id)

    def __repr__(self):
        return (
            f"<Reserve"
            f" id={self.id}"
            f" size={self.size}"
            f" update_method={self.update_method}"
            f" wallet_id={self.wallet_id}>"
        )

    def to_dto(self) -> dto.Reserve:
        return dto.Reserve(
            id=self.id,
            size=self.size,
            update_method=self.update_method,
            wallet_id=self.wallet_id
        )
