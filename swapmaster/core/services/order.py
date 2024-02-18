from datetime import datetime

from swapmaster.core.constants import OrderStatusEnum
from swapmaster.core.models import Order, PairId, UserId, Requisite
from swapmaster.core.models.order import OrderWithRequisites


class OrderService:
    def create_service(
        self,
        pair_id: PairId,
        user_id: UserId,
        to_receive: float,
        to_send: float
    ) -> Order:
        return Order(
            order_id=None,
            pair_id=pair_id,
            user_id=user_id,
            to_receive=to_receive,
            to_send=to_send,
            date_start=datetime.now(),
            date_finish=None,
            status=OrderStatusEnum.PROCESSING
        )

    def add_requisites(self, order: Order, requisites: list[Requisite]) -> OrderWithRequisites:
        return OrderWithRequisites(
            order_id=order.order_id,
            pair_id=order.pair_id,
            user_id=order.user_id,
            to_receive=order.to_receive,
            to_send=order.to_send,
            date_start=order.date_start,
            date_finish=order.date_finish,
            status=order.status,
            requisites=requisites
        )
