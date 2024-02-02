from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import Base


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

    method_from: Mapped["Method"] = relationship(foreign_keys=method_from_id)
    method_to: Mapped["Method"] = relationship(foreign_keys=method_to_id)
    commission: Mapped["Commission"] = relationship()

    def __repr__(self):
        return (
            f"<Pair id={self.id}"
            f" method_from_id={self.method_from_id}"
            f" method_to_id={self.method_to_id}"
            f" commission_id={self.commission_id}>"
        )