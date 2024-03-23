from dataclasses import dataclass, field

from swapmaster.common.config.models.central import CentralConfig


@dataclass
class CentralConfigMock(CentralConfig):
    order_payment_expire_minutes: int = field(
        default=30, init=False
    )
