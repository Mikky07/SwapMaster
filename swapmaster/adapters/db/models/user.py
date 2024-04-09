from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import ENUM, BIGINT

from swapmaster.core.constants import VerificationStatusEnum
from swapmaster.adapters.db.models import Base
from swapmaster.core import models as dto


class UserExtraData(Base):
    __tablename__ = "users_extra_data"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BIGINT)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped['User'] = relationship(foreign_keys=user_id, back_populates="extra_data")


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
            verification_status=self.verification_status,
        )
