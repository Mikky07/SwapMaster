from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import Base


class Course(Base):
    __tablename__ = "courses"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[float]

    pair_id: Mapped[int] = mapped_column(ForeignKey("pairs.id", ondelete="CASCADE"))
    pair: Mapped["Pair"] = relationship(foreign_keys=pair_id)

    def __repr__(self):
        return (
            f"<Course id={self.id}"
            f" value={self.value}"
            f" pair_id={self.pair_id}>"
        )
