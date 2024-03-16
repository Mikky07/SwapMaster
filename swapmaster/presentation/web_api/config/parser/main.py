from swapmaster.adapters.mq.notification.config import load_email_config
from swapmaster.common.config.models import Paths
from swapmaster.common.config.parser import read_config, load_config
from swapmaster.presentation.web_api.config.models.main import APIConfig
from swapmaster.presentation.web_api.config.parser.auth import load_auth_config


def load_api_config(paths: Paths) -> APIConfig:
    config_dct = read_config(paths)
    return APIConfig.from_base(
        base=load_config(config_dct),
        auth=load_auth_config(config_dct.get("auth")),
        email=load_email_config(config_dct.get("email"))
    )
