from ..models.central import CentralConfig


def load_central_config(dct: dict) -> CentralConfig:
    return CentralConfig(
        order_payment_expire_minutes=dct.get("order-payment-expire-minutes", 20)
    )
