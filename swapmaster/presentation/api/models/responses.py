from pydantic import BaseModel

from swapmaster.core.models import Order, OrderRequisite


class FullOrder(BaseModel):
    order: Order
    order_requisites: list[OrderRequisite]
