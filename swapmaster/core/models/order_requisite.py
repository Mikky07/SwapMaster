from typing import TypeAlias, Optional
from dataclasses import dataclass

from .order import OrderId
from .requisite import RequisiteId

OrderRequisiteId: TypeAlias = int


@dataclass(slots=True)
class OrderRequisite:
    id: Optional[OrderRequisiteId]
    order_id: 'OrderId'
    requisite_id: 'RequisiteId'
    data: str
