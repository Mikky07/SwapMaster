from dataclasses import dataclass

from swapmaster.core.models import PairId, UserId, OrderRequisite


@dataclass
class NewOrderRequestDTO:
    pair_id: PairId
    user_id: UserId
    to_receive: float
    requisites: list[OrderRequisite]
