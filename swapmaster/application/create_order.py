import asyncio
from dataclasses import dataclass

from swapmaster.application.common.protocols import (
    RequisiteReader,
    OrderRequisiteWriter,
    NewOrderRequisiteDTO, PairReader
)
from swapmaster.core.models import Order, PairId, UserId
from swapmaster.core.services.order import OrderService
from .common.protocols import OrderWriter, ReserveReader
from .common.uow import UoW
from .common.interactor import Interactor
from ..core.utils.exceptions import SMError


@dataclass
class NewOrderDTO:
    pair_id: PairId
    user_id: UserId
    to_receive: float
    to_send: float
    requisites: list[NewOrderRequisiteDTO]


class AddOrder(Interactor[NewOrderDTO, Order]):
    def __init__(
        self,
        uow: UoW,
        order_gateway: OrderWriter,
        order_service: OrderService,
        pair_gateway: PairReader,
        requisites_gateway: RequisiteReader,
        order_requisite_gateway: OrderRequisiteWriter,
        reserve_gateway: ReserveReader
    ):
        self.reserve_gateway = reserve_gateway
        self.pair_gateway = pair_gateway
        self.order_gateway = order_gateway
        self.uow = uow
        self.order_service = order_service
        self.requisites_gateway = requisites_gateway
        self.order_requisite_gateway = order_requisite_gateway

    async def __call__(self, data: NewOrderDTO) -> Order:
        pair = await self.pair_gateway.get_pair_by_id(pair_id=data.pair_id)
        reserve = await self.reserve_gateway.get_reserve_of_method(method_id=pair.method_to)
        if reserve.size < data.to_receive:
            raise SMError("Reserve size is less than you want to convert")
        new_order: Order = self.order_service.create_service(
            pair_id=data.pair_id,
            user_id=data.user_id,
            to_receive=data.to_receive,
            to_send=data.to_send
        )
        order_saved = await self.order_gateway.add_order(order=new_order)
        await self.uow.commit()
        if order_saved:
            tasks = [
                self.order_requisite_gateway.add_order_requisite(
                    order_requisite=requisite,
                    order_id=order_saved.id
                )
                for requisite in data.requisites
            ]
            await asyncio.gather(*tasks)
        await self.uow.commit()
        return order_saved
