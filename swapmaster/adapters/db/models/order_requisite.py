from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .base import Base
from swapmaster.core import models as dto


class OrderRequisite(Base):
    __tablename__ = 'order_requisite'
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data: Mapped[str]

    order_id = mapped_column(ForeignKey("orders.id"))
    order: Mapped['Order'] = relationship()

    requisite_id = mapped_column(ForeignKey("requisites.id"))
    requisite: Mapped['Requisite'] = relationship()

    def __repr__(self):
        return (
            f"<OrderRequisite "
            f" id={self.id}"
            f" data={self.data}"
            f" order_id={self.order_id}"
            f" requisite_id={self.requisite_id}>"
        )

    def to_dto(self) -> dto.OrderRequisite:
        return dto.OrderRequisite(
            id=self.id,
            data=self.data,
            order_id=self.order_id,
            requisite_id=self.requisite_id
        )
