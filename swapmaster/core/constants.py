from enum import Enum


class OrderStatusEnum(Enum):
    PROCESSING = "PROCESSING"
    FINISHED = "FINISHED"


class ReserveUpdateMethodEnum(Enum):
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"
