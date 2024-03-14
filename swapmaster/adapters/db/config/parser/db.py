from swapmaster.adapters.db.config.models import DBConfig
from swapmaster.adapters.db.config.models.db import RedisConfig


def load_db_config(db_dict: dict) -> DBConfig:
    return DBConfig(
        dialect=db_dict.get("dialect", "postgresql"),
        driver=db_dict.get("driver", "psycopg2"),
        user=db_dict.get("user", "postgres"),
        password=db_dict.get("password", "postgres"),
        host=db_dict.get("host", "localhost"),
        port=db_dict.get("port", 5432),
        database=db_dict.get("database", "postgres")
    )


def load_redis_config(dct: dict) -> RedisConfig:
    return RedisConfig(
        host=dct.get("host", "localhost"),
        port=dct.get("port", 6379)
    )
