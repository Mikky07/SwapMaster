from sqlalchemy.orm import mapped_column, Mapped

from .base import Base
from swapmaster.core import models as dto


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    def __repr__(self):
        return (
            f"<User"
            f" id={self.id}"
            f" username={self.username}"
            f" hashed_password={self.hashed_password}>"
        )

    def to_dto(self) -> dto.User:
        return dto.User(
            id=self.id,
            username=self.username,
            hashed_password=self.hashed_password
        )
