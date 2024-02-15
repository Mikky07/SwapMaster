from datetime import datetime

from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.protocols.order_gateway import OrderUpdater
from swapmaster.application.common.uow import UoW
from swapmaster.core.models import OrderId, Order


class FinishOrder(Interactor[OrderId, Order]):
    def __init__(
            self,
            uow: UoW,
            order_gateway: OrderUpdater
    ):
        self.uow = uow
        self.order_gateway = order_gateway

    async def __call__(self, data: OrderId) -> Order:
        # check if that order is already finished
        order_finished = await self.order_gateway.finish_order(
            order_id=data,
            date_finish=datetime.now()
        )
        # some logic to notify user
        await self.uow.commit()
        return order_finished
