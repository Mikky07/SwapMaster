from ..models import Config
from swapmaster.adapters.db.config.parser import load_db_config


def load_config(config_dict: dict) -> Config:
    return Config(
        db=load_db_config(db_dict=config_dict.get("db"))
    )
