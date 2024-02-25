from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import ENUM

from swapmaster.core.constants import VerificationStatusEnum
from .base import Base
from swapmaster.core import models as dto


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    verification_status: Mapped[VerificationStatusEnum] = mapped_column(
        ENUM(VerificationStatusEnum), default=VerificationStatusEnum.UNVERIFIED
    )

    def __repr__(self):
        return (
            f"<User"
            f" id={self.id}"
            f" email={self.email}"
            f" username={self.username}"
            f" hashed_password={self.hashed_password}"
            f" verification_status={self.verification_status}>"
        )

    def to_dto(self) -> dto.User:
        return dto.User(
            id=self.id,
            username=self.username,
            hashed_password=self.hashed_password,
            email=self.email,
            verification_status=self.verification_status
        )
