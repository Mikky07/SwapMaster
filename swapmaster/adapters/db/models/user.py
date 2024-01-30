from .base import Base
from sqlalchemy.orm import mapped_column, Mapped


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager-defaults": True}

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
