from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM

from .base import Base
from swapmaster.core.constants import CourseObtainingMethod


class Pair(Base):
    __tablename__ = "pairs"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_obtaining_method: Mapped[CourseObtainingMethod] = mapped_column(
        ENUM(CourseObtainingMethod),
        default=CourseObtainingMethod.STATIC
    )

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
            f" course_obtaining_method={self.course_obtaining_method}"
            f" method_from_id={self.method_from_id}"
            f" method_to_id={self.method_to_id}"
            f" commission_id={self.commission_id}>"
        )
