from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM

from swapmaster.core import models as dto
from .base import Base
from swapmaster.core.constants import OrderStatusEnum


class Order(Base):
    __tablename__ = "orders"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pair_id: Mapped[int] = mapped_column(ForeignKey("pairs.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    to_receive: Mapped[float]
    to_send: Mapped[float]
    date_start: Mapped[datetime]
    date_finish: Mapped[Optional[datetime]]
    status: Mapped[OrderStatusEnum] = mapped_column(
        ENUM(OrderStatusEnum),
        default=OrderStatusEnum.PROCESSING
    )

    pair: Mapped["Pair"] = relationship(foreign_keys=pair_id)
    user: Mapped["User"] = relationship(foreign_keys=user_id)

    def __repr__(self):
        return (
            f"<Order id={self.id}"
            f" pair_id={self.pair_id}"
            f" user_id={self.user_id}"
            f" to_receive={self.to_receive}"
            f" to_send={self.to_send}"
            f" date_start={self.date_start}"
            f" date_finish={self.date_finish}"
            f" status={self.status}"
        )

    def to_dto(self) -> dto.Order:
        return dto.Order(
            id=self.id,
            pair_id=self.pair_id,
            user_id=self.user_id,
            to_receive=self.to_receive,
            to_send=self.to_send,
            date_start=self.date_start,
            date_finish=self.date_finish,
            status=self.status
        )
