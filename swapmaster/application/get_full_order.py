from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.protocols.order_gateway import OrderReader
from swapmaster.application.common.protocols.requisite_gateway import RequisiteReader
from swapmaster.core.models import Requisite
from swapmaster.core.models.order import OrderId, OrderWithRequisites
from swapmaster.core.services.order import OrderService


class GetFullOrder(Interactor[OrderId, OrderWithRequisites]):
    def __init__(
            self,
            order_gateway: OrderReader,
            requisite_gateway: RequisiteReader,
            order_service: OrderService
    ):
        self.order_gateway = order_gateway
        self.order_service = order_service
        self.requisite_gateway = requisite_gateway

    async def __call__(self, data: OrderId) -> OrderWithRequisites:
        order = await self.order_gateway.get_order(order_id=data)
        order_requisites: list[Requisite] = await self.requisite_gateway.get_requisites_of_order(order_id=data)
        order_with_requisites = self.order_service.add_requisites(
            order=order,
            requisites=order_requisites
        )
        return order_with_requisites
