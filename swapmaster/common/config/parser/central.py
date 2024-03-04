from ..models.central import CentralConfig


def load_central_config(dct: dict) -> CentralConfig:
    return CentralConfig(
        expire_minutes=dct.get("expire-minutes", 20)
    )
