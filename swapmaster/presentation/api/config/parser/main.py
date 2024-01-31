from swapmaster.common.config.models import Config, Paths
from swapmaster.common.config.parser import read_config, load_config


# stub
def load_api_config(paths: Paths) -> Config:
    config_dct = read_config(paths)
    return load_config(config_dct)
