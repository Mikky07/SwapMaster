from swapmaster.common.config.models import Paths
from swapmaster.common.config.parser import read_config
from swapmaster.presentation.api.config.models.main import APIConfig
from swapmaster.presentation.api.config.parser.auth import load_auth_config
from swapmaster.adapters.db.config.parser.db import load_db_config


def load_api_config(paths: Paths) -> APIConfig:
    config_dct = read_config(paths)
    return APIConfig(
        auth=load_auth_config(config_dct.get("auth")),
        db=load_db_config(config_dct.get("db"))
    )
