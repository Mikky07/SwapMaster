from dataclasses import dataclass

from swapmaster.adapters.db.config.models import DBConfig, RedisConfig


@dataclass
class Config:
    db: DBConfig
    redis: RedisConfig
