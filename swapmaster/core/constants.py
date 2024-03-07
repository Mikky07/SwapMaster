from enum import Enum


class OrderStatusEnum(Enum):
    PROCESSING = "PROCESSING"
    CANCELED = "CANCELED"
    FINISHED = "FINISHED"


class CourseUpdateMethodEnum(Enum):
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"


class ReserveUpdateMethodEnum(Enum):
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"


class VerificationStatusEnum(Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"


class OrderPaymentStatusEnum(Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"
