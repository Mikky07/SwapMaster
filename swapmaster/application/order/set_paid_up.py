from swapmaster.application.common.uow import UoW
from swapmaster.application.common.gateways import OrderUpdater
from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.task_manager import TaskManager
from swapmaster.core.models import OrderId, Order


class SetOrderPaidUp(Interactor[OrderId, Order]):
    def __init__(
            self,
            uow: UoW,
            order_gateway: OrderUpdater,
            task_manager: TaskManager
    ):
        self.uow = uow
        self.order_gateway = order_gateway
        self.task_manager = task_manager

    async def __call__(self, order_id: OrderId) -> Order:
        await self.task_manager.remove_async_task(task_id=str(order_id))
        order_paid = await self.order_gateway.set_as_paid(order_id=order_id)
        await self.uow.commit()
        return order_paid
