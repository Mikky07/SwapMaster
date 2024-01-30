from dataclasses import dataclass

from swapmaster.adapters.db.config.models import DBConfig


@dataclass
class Config:
    db: DBConfig
