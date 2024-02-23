from datetime import datetime

from .common import UoW
from .common.interactor import Interactor
from swapmaster.application.common.protocols import OrderUpdater
from swapmaster.core.models import OrderId, Order


class CancelOrder(Interactor[OrderId, Order]):
    def __init__(
            self,
            uow: UoW,
            order_gateway: OrderUpdater
    ):
        self.uow = uow
        self.order_gateway = order_gateway

    async def __call__(self, data: OrderId) -> Order:
        cancel_date = datetime.now()
        order_canceled = await self.order_gateway.cancel_order(order_id=data, date_cancel=cancel_date)
        # some logic to notify user
        await self.uow.commit()
        return order_canceled
