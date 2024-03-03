from datetime import datetime

from swapmaster.application.common import Notifier
from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.db import (
    OrderUpdater,
    OrderReader,
    ReserveUpdater,
    ReserveReader,
    PairReader, UserReader
)
from swapmaster.application.common.uow import UoW
from swapmaster.core.models import OrderId, Order


class FinishOrder(Interactor[OrderId, Order]):
    def __init__(
            self,
            uow: UoW,
            order_gateway: OrderUpdater | OrderReader,
            reserve_gateway: ReserveUpdater | ReserveReader,
            pair_reader: PairReader,
            user_reader: UserReader,
            notifier: Notifier
    ):
        self.uow = uow
        self.order_gateway = order_gateway
        self.reserve_gateway = reserve_gateway
        self.pair_reader = pair_reader
        self.user_reader = user_reader
        self.notifier = notifier

    async def __call__(self, data: OrderId) -> Order:
        order = await self.order_gateway.get_order(order_id=data)
        pair = await self.pair_reader.get_pair_by_id(pair_id=order.pair_id)
        reserve_of_method_to = await self.reserve_gateway.get_reserve_of_method(method_id=pair.method_to)
        reserve_of_method_from = await self.reserve_gateway.get_reserve_of_method(method_id=pair.method_from)
        await self.reserve_gateway.update_reserve_size(
            reserve_id=reserve_of_method_to.id,
            size=reserve_of_method_to.size - order.to_receive
        )
        await self.reserve_gateway.update_reserve_size(
            reserve_id=reserve_of_method_from.id,
            size=reserve_of_method_from.size + order.to_send
        )
        order_finished = await self.order_gateway.finish_order(
            order_id=data,
            date_finish=datetime.now()
        )
        await self.uow.commit()
        customer = await self.user_reader.get_user(user_id=order_finished.user_id)
        self.notifier.notify(
            user=customer,
            notification="Order successfully finished.",
            subject="Order finished"
        )
        return order_finished
