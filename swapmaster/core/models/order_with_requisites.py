from dataclasses import dataclass

from .order import Order
from .order_requisite import OrderRequisite


@dataclass(slots=True)
class OrderWithRequisites:
    order: Order
    requisites: list[OrderRequisite]
