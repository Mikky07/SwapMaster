from datetime import datetime

from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.db import (
    OrderUpdater,
    OrderReader,
    ReserveUpdater,
    ReserveReader,
    PairReader
)
from swapmaster.application.common.uow import UoW
from swapmaster.core.models import OrderId, Order


class FinishOrder(Interactor[OrderId, Order]):
    def __init__(
            self,
            uow: UoW,
            order_updater: OrderUpdater,
            order_reader: OrderReader,
            reserve_updater: ReserveUpdater,
            reserve_reader: ReserveReader,
            pair_reader: PairReader
    ):
        self.uow = uow
        self.order_updater = order_updater
        self.order_reader = order_reader
        self.reserve_reader = reserve_reader
        self.reserve_updater = reserve_updater
        self.pair_reader = pair_reader

    async def __call__(self, data: OrderId) -> Order:
        order = await self.order_reader.get_order(order_id=data)
        pair = await self.pair_reader.get_pair_by_id(pair_id=order.pair_id)
        reserve_of_method_to = await self.reserve_reader.get_reserve_of_method(method_id=pair.method_to)
        reserve_of_method_from = await self.reserve_reader.get_reserve_of_method(method_id=pair.method_from)
        await self.reserve_updater.update_reserve_size(
            reserve_id=reserve_of_method_to.id,
            size=reserve_of_method_to.size - order.to_receive
        )
        await self.reserve_updater.update_reserve_size(
            reserve_id=reserve_of_method_from.id,
            size=reserve_of_method_from.size + order.to_send
        )
        order_finished = await self.order_updater.finish_order(
            order_id=data,
            date_finish=datetime.now()
        )
        # some logic to notify user
        await self.uow.commit()
        return order_finished
