from enum import Enum


class OrderStatusEnum(Enum):
    PROCESSING = "PROCESSING"
    UNFULFILLED = "UNFULFILLED"
    FINISHED = "FINISHED"


class CourseUpdateMethodEnum(Enum):
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"


class ReserveUpdateMethodEnum(Enum):
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"
