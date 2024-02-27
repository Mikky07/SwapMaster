from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.db import (
    OrderReader,
    RequisiteReader,
    OrderRequisiteReader
)
from swapmaster.core.models.order import OrderId
from swapmaster.core.models.order_with_requisites import OrderWithRequisites
from swapmaster.core.services.order import OrderService


class GetFullOrder(Interactor[OrderId, OrderWithRequisites]):
    def __init__(
            self,
            order_gateway: OrderReader,
            requisite_gateway: RequisiteReader,
            order_service: OrderService,
            order_requisite_gateway: OrderRequisiteReader
    ):
        self.order_gateway = order_gateway
        self.order_service = order_service
        self.requisite_gateway = requisite_gateway
        self.order_requisite_gateway = order_requisite_gateway

    async def __call__(self, data: OrderId) -> OrderWithRequisites:
        order = await self.order_gateway.get_order(order_id=data)
        order_requisites = await self.order_requisite_gateway.get_order_requisites(order_id=order.id)
        return OrderWithRequisites(
            order=order,
            requisites=order_requisites
        )
