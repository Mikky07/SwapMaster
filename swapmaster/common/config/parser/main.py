from ..models import Config
from swapmaster.adapters.db.config.parser import load_db_config, load_redis_config
from swapmaster.common.config.parser.central import load_central_config


def load_config(config_dict: dict) -> Config:
    return Config(
        db=load_db_config(db_dict=config_dict.get("db")),
        redis=load_redis_config(dct=config_dict.get("redis")),
        central=load_central_config(dct=config_dict.get("central"))
    )
