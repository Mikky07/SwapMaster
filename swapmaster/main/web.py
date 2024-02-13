import uvicorn

from swapmaster.common.config.models import Paths
from swapmaster.common.config.parser import get_paths
from swapmaster.presentation.api import *


app = setup()


def get_paths_common() -> Paths:
    return get_paths("API_PATH")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
