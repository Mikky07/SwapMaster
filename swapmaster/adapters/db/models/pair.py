import typing
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from swapmaster.core import models as dto
from swapmaster.adapters.db.models import Base

if typing.TYPE_CHECKING:
    from swapmaster.adapters.db.models import Requisite


class Pair(Base):
    __tablename__ = "pairs"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    method_from_id = mapped_column(
        ForeignKey("methods.id", ondelete="CASCADE")
    )
    method_to_id = mapped_column(
        ForeignKey("methods.id", ondelete="CASCADE")
    )
    commission_id = mapped_column(
        ForeignKey("commissions.id")
    )
    course_id = mapped_column(
        ForeignKey("courses.id")
    )
    reception_wallet_id = mapped_column(
        ForeignKey("wallets.id")
    )

    method_from = relationship("Method", foreign_keys=method_from_id)
    method_to = relationship("Method", foreign_keys=method_to_id)
    commission = relationship("Commission", foreign_keys=commission_id)
    course = relationship("Course", foreign_keys=course_id)
    reception_wallet = relationship("Wallet", foreign_keys=reception_wallet_id)

    requisites: Mapped[Optional[list['Requisite']]] = relationship(back_populates="pair")

    def __repr__(self):
        return (
            f"<Pair id={self.id}"
            f" method_from_id={self.method_from_id}"
            f" method_to_id={self.method_to_id}"
            f" commission_id={self.commission_id}"
            f" course_id={self.course_id}"
            f" reception_wallet_id={self.reception_wallet_id}>"
        )

    def to_dto(self) -> dto.Pair:
        return dto.Pair(
            id=self.id,
            method_from=self.method_from_id,
            method_to=self.method_to_id,
            commission=self.commission_id,
            course_id=self.course_id,
            reception_wallet=self.reception_wallet_id
        )
