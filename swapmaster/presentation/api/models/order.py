from dataclasses import dataclass

from swapmaster.core.models import PairId, UserId
from swapmaster.application.common.db import NewOrderRequisiteDTO


@dataclass
class NewOrderRequestDTO:
    pair_id: PairId
    user_id: UserId
    to_receive: float
    requisites: list[NewOrderRequisiteDTO]
