from datetime import datetime

from swapmaster.core.constants import OrderStatusEnum
from swapmaster.core.models import Order, PairId, UserId


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
