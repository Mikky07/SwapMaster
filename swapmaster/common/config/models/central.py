from dataclasses import dataclass


@dataclass
class CentralConfig:
    order_payment_expire_minutes: int
