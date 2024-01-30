import uvicorn
from fastapi import FastAPI

from swapmaster.common.config.parser import logging_setup
from swapmaster.presentation.api.main_factory import create_app, get_paths_common


def main() -> FastAPI:
    paths = get_paths_common()

    logging_setup(paths=paths)

    app = create_app()

    return app


if __name__ == '__main__':
    uvicorn.run(main(), host='127.0.0.1', port=8000)
