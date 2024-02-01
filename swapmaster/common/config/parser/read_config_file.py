import yaml

from ..models import Paths


def read_config(paths: Paths) -> dict:
    with open(paths.get_config_dir / "config.yml", "r") as config_file:
        return yaml.safe_load(config_file)
