from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    pair: Mapped["Pair"] = relationship(back_populates="course")

    def __repr__(self):
        return (
            f"<Course id={self.id}"
            f" value={self.value}"
            f" update_method={self.update_method}>"
        )
