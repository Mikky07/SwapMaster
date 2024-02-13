from fastapi import FastAPI

from swapmaster.common.config.parser import logging_setup
from swapmaster.main.web import get_paths_common
from swapmaster.presentation.api.config.parser.main import load_api_config
from swapmaster.presentation.api.factory import create_app


def setup() -> FastAPI:
    paths = get_paths_common()

    api_config = load_api_config(paths=paths)
    logging_setup(paths=paths)

    app = create_app(api_config)

    return app
