from enum import Enum


class OrderStatusEnum(Enum):
    PROCESSING = "PROCESSING"
    FINISHED = "FINISHED"


class CourseObtainingMethod(Enum):
    STATIC = "STATIC"
    STOCK_EXCHANGE_SERVICE = "STOCK_EXCHANGE_SERVICE"
