from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import Base
from swapmaster.core.constants import CourseUpdateMethodEnum


class Course(Base):
    __tablename__ = "courses"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[float]
    update_method: Mapped[CourseUpdateMethodEnum] = mapped_column(
        ENUM(CourseUpdateMethodEnum)
    )

    pair_id: Mapped[int] = mapped_column(ForeignKey("pairs.id", ondelete="CASCADE"))
    pair: Mapped["Pair"] = relationship(foreign_keys=pair_id)

    def __repr__(self):
        return (
            f"<Course id={self.id}"
            f" value={self.value}"
            f" pair_id={self.pair_id}"
            f" update_method={self.update_method}>"
        )
