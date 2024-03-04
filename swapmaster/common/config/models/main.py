from dataclasses import dataclass

from swapmaster.adapters.db.config.models import DBConfig, RedisConfig
from swapmaster.common.config.models.central import CentralConfig


@dataclass
class Config:
    db: DBConfig
    redis: RedisConfig
    central: CentralConfig
