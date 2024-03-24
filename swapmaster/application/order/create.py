import asyncio
from datetime import datetime, timedelta
from dataclasses import dataclass

from swapmaster.application.common import Notifier
from swapmaster.application.common.gateways import (
    RequisiteReader,
    OrderRequisiteWriter,
    PairReader,
    OrderWriter,
    ReserveReader,
    UserReader,
    OrderUpdater,
    MethodReader
)
from swapmaster.application.common.task_manager import AsyncTaskManager
from swapmaster.application.order.cancel import cancel_expired_order
from swapmaster.common.config.models.central import CentralConfig
from swapmaster.core.models import Order, PairId, UserId, OrderRequisite, OrderId
from swapmaster.core.services.order import OrderService
from swapmaster.application.common.uow import UoW
from swapmaster.application.common.interactor import Interactor
from swapmaster.core.services.requisite import RequisiteService
from swapmaster.core.utils.exceptions import (
    RequisitesNotValid,
    OrderCreationError
)


@dataclass
class NewOrderDTO:
    pair_id: PairId
    user_id: UserId
    to_receive: float
    to_send: float
    requisites_filled: list[OrderRequisite]


@dataclass
class CreatedOrderDTO:
    order: Order
    payment_expires_at: datetime


class CreateOrder(Interactor):
    def __init__(
        self,
        uow: UoW,
        order_gateway: OrderWriter | OrderUpdater,
        user_gateway: UserReader,
        order_service: OrderService,
        requisite_service: RequisiteService,
        pair_gateway: PairReader,
        requisite_gateway: RequisiteReader,
        order_requisite_gateway: OrderRequisiteWriter,
        reserve_gateway: ReserveReader,
        notifier: Notifier,
        task_manager: AsyncTaskManager,
        method_gateway: MethodReader,
        config: CentralConfig,
    ):
        self.reserve_gateway = reserve_gateway
        self.pair_gateway = pair_gateway
        self.user_gateway = user_gateway
        self.method_gateway = method_gateway
        self.order_gateway = order_gateway
        self.uow = uow
        self.order_service = order_service
        self.requisite_service = requisite_service
        self.requisite_gateway = requisite_gateway
        self.order_requisite_gateway = order_requisite_gateway
        self.notifier = notifier
        self.task_manager = task_manager
        self.config = config

    async def add_filled_requisites(self, order_id: OrderId, requisites_filled: list[OrderRequisite]):
        tasks = []

        for requisite in requisites_filled:
            task = self.order_requisite_gateway.add_order_requisite(
                    order_requisite=requisite,
                    order_id=order_id
            )
            tasks.append(task)

        await asyncio.gather(*tasks)

    async def __call__(self, data: NewOrderDTO) -> CreatedOrderDTO:
        pair = await self.pair_gateway.get_pair_by_id(pair_id=data.pair_id)
        method_to = await self.method_gateway.get_method_by_id(method_id=pair.method_to_id)
        reserve = await self.reserve_gateway.get_reserve_by_id(reserve_id=method_to.reserve_id)

        if reserve.size < data.to_receive:
            raise OrderCreationError("Reserve size is less than you want to convert")

        pair_requisites = await self.requisite_gateway.get_requisites_of_pair(
            pair_id=data.pair_id
        )

        if not self.requisite_service.check_requisites_validity(
            pair_requisites=pair_requisites,
            order_requisites=data.requisites_filled
        ):
            raise RequisitesNotValid("Requisites that you have filled is not valid!")

        new_order: Order = self.order_service.create_order(
            pair_id=data.pair_id,
            user_id=data.user_id,
            to_receive=data.to_receive,
            to_send=data.to_send
        )
        order_saved = await self.order_gateway.add_order(order=new_order)

        if order_saved:
            await self.add_filled_requisites(order_id=order_saved.id, requisites_filled=data.requisites_filled)
        else:
            raise OrderCreationError("Some issues happened during order creation")

        await self.uow.commit()

        order_expiration_date = (
                datetime.now() + timedelta(minutes=self.config.order_payment_expire_minutes)
        )

        customer = await self.user_gateway.get_user_by_id(user_id=order_saved.user_id)

        self.notifier.notify(
            user=customer,
            notification=f"Order {order_saved.id} successfully created.",
            subject="Order created"
        )

        await self.task_manager.plan_task(
            task=cancel_expired_order,
            task_id=f"cancel-order:{order_saved.id}",
            run_date=order_expiration_date,
            order_id=order_saved.id,
            notification="Your order have been canceled because of expiration"
        )

        return CreatedOrderDTO(
            order=order_saved,
            payment_expires_at=order_expiration_date
        )
