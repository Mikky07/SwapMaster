from pathlib import Path
from dataclasses import dataclass


@dataclass
class Paths:
    app_dir: Path

    @property
    def get_config_dir(self) -> Path:
        return self.app_dir / "config"

    @property
    def get_log_dir(self) -> Path:
        return self.app_dir / "config"
