import os
from pathlib import Path

from ..models import Paths


def get_paths(env_path_var: str) -> Paths:
    if path := os.getenv(env_path_var, None):
        return Paths(Path(path))
    return Paths(app_dir=Path(__file__).parent.parent.parent.parent.parent)
