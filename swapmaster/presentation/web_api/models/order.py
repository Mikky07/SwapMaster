from dataclasses import dataclass

from swapmaster.application.common.db import NewOrderRequisiteDTO
from swapmaster.core.models import PairId, UserId


@dataclass
class NewOrderRequestDTO:
    pair_id: PairId
    user_id: UserId
    to_receive: float
    requisites: list[NewOrderRequisiteDTO]
