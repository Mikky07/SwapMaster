from dataclasses import dataclass
from typing import Optional, TypeAlias
from datetime import datetime

from swapmaster.core.constants import OrderStatusEnum
from .user import UserId
from .pair import PairId


OrderId: TypeAlias = int


@dataclass
class Order:
    id: Optional[OrderId]
    pair_id: PairId
    user_id: UserId
    to_receive: float
    to_send: float
    date_start: Optional[datetime]
    date_finish: Optional[datetime]
    status: OrderStatusEnum



