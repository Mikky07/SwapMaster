from typing import Optional

from sqlalchemy import BIGINT
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import ENUM

from swapmaster.core.constants import VerificationStatusEnum
from swapmaster.adapters.db.models import Base
from swapmaster.core import models as dto


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[Optional[str]] = mapped_column(unique=True)
    hashed_password: Mapped[Optional[str]]
    tg_id: Mapped[Optional[int]] = mapped_column(BIGINT, unique=True)
    verification_status: Mapped[VerificationStatusEnum] = mapped_column(
        ENUM(VerificationStatusEnum), default=VerificationStatusEnum.UNVERIFIED
    )

    def __repr__(self):
        return (
            f"<User"
            f" id={self.id}"
            f" email={self.email}"
            f" username={self.username}"
            f" tg_id={self.tg_id}"
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
            tg_id=self.tg_id
        )
