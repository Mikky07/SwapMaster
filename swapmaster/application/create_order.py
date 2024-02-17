from dataclasses import dataclass

from swapmaster.core.models import Order, PairId, UserId
from swapmaster.core.services.order import OrderService
from .common.protocols.order_gateway import OrderWriter
from .common.uow import UoW
from .common.interactor import Interactor


@dataclass
class NewOrderDTO:
    pair_id: PairId
    user_id: UserId
    to_receive: float
    to_send: float


class AddOrder(Interactor[NewOrderDTO, Order]):
    def __init__(
        self,
        uow: UoW,
        order_gateway: OrderWriter,
        order_service: OrderService
    ):
        self.order_gateway = order_gateway
        self.uow = uow
        self.order_service = order_service

    async def __call__(self, data: NewOrderDTO) -> Order:
        # have to add fetching requisites
        new_order: Order = self.order_service.create_service(
            pair_id=data.pair_id,
            user_id=data.user_id,
            to_receive=data.to_receive,
            to_send=data.to_send
        )
        order_saved = await self.order_gateway.add_order(order=new_order)
        await self.uow.commit()
        return order_saved
