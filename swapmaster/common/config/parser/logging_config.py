import logging.config

import yaml

from ..models import Paths


def logging_setup(paths: Paths):
    print(paths.get_log_dir)
    with open(paths.get_log_dir / "logging.yml", "r") as log_dir:
        log_dict = yaml.safe_load(log_dir)
    logging.config.dictConfig(log_dict)
    logging.info("Logging set up successfully!")
