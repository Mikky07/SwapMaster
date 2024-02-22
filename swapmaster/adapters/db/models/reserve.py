from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship, mapped_column, Mapped

from swapmaster.core.constants import ReserveUpdateMethodEnum
from swapmaster.core import models as dto
from .base import Base


class Reserve(Base):
    __tablename__ = "reserves"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    size: Mapped[float]
    update_method: Mapped[ReserveUpdateMethodEnum] = mapped_column(
        ENUM(ReserveUpdateMethodEnum)
    )

    method_id = mapped_column(ForeignKey("methods.id"))
    method: Mapped['Method'] = relationship(back_populates="reserve", foreign_keys=method_id)

    wallet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wallets.id"))
    wallet: Mapped[Optional['Wallet']] = relationship(back_populates="reserve", foreign_keys=wallet_id)

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
