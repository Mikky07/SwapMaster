from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime

import aiohttp

from swapmaster.application.common import UoW, Notifier
from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.db import OrderUpdater, UserReader
from swapmaster.core.models import OrderId, Order


@dataclass(slots=True)
class CancelOrderDTO:
    order_id: OrderId
    notification: str


class CancelOrder(Interactor[CancelOrderDTO, Order]):
    def __init__(
            self,
            uow: UoW,
            order_updater: OrderUpdater,
            user_reader: UserReader,
            notifier: Notifier
    ):
        self.uow = uow
        self.order_updater = order_updater
        self.user_reader = user_reader
        self.notifier = notifier

    async def __call__(self, data: CancelOrderDTO) -> Order:
        cancel_date = datetime.now()
        order_canceled = await self.order_updater.cancel_order(
            order_id=data.order_id,
            date_cancel=cancel_date
        )
        await self.uow.commit()
        customer = await self.user_reader.get_user(user_id=order_canceled.user_id)
        self.notifier.notify(
            user=customer,
            notification=data.notification,
            subject="Order canceled"
        )
        return order_canceled


class OrderCancelerFactory:
    @asynccontextmanager
    async def order_canceler(self) -> CancelOrder:
        raise NotImplementedError

