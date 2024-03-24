from swapmaster.application.common.uow import UoW
from swapmaster.application.common.gateways import OrderUpdater
from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.task_manager import AsyncTaskManager
from swapmaster.core.models import OrderId, Order


class SetOrderPaidUp(Interactor):
    def __init__(
            self,
            uow: UoW,
            order_gateway: OrderUpdater,
            task_manager: AsyncTaskManager
    ):
        self.uow = uow
        self.order_gateway = order_gateway
        self.task_manager = task_manager

    async def __call__(self, order_id: OrderId) -> Order:
        await self.task_manager.remove_planned_task(f"cancel-order:{order_id}")

        order_paid = await self.order_gateway.set_as_paid(order_id=order_id)
        await self.uow.commit()

        return order_paid
