from dataclasses import dataclass
from datetime import datetime

from swapmaster.application.common import UoW, Notifier
from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.gateways import OrderUpdater, UserReader
from swapmaster.core.models import OrderId, Order


@dataclass(slots=True)
class CancelOrderDTO:
    order_id: OrderId
    notification: str


class CancelOrder(Interactor[CancelOrderDTO, Order]):
    def __init__(
            self,
            uow: UoW,
            order_gateway: OrderUpdater,
            user_gateway: UserReader,
            notifier: Notifier
    ):
        self.uow = uow
        self.order_updater = order_gateway
        self.user_reader = user_gateway
        self.notifier = notifier

    async def __call__(self, data: CancelOrderDTO) -> Order:
        cancel_date = datetime.now()

        order_canceled = await self.order_updater.cancel_order(
            order_id=data.order_id,
            date_canceled=cancel_date
        )

        await self.uow.commit()

        customer = await self.user_reader.get_user_by_id(user_id=order_canceled.user_id)
        self.notifier.notify(
            user=customer,
            notification=data.notification,
            subject="Order canceled"
        )

        return order_canceled


async def cancel_expired_order(
        order_canceller: CancelOrder,
        order_id: OrderId,
        notification: str,
):
    await order_canceller(
        data=CancelOrderDTO(
            order_id=order_id,
            notification=notification
        )
    )
