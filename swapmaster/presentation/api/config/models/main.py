from dataclasses import dataclass

from swapmaster.adapters.mq.notification.config import EmailConfig
from swapmaster.common.config.models import Config
from swapmaster.presentation.api.config.models.auth import AuthConfig


@dataclass
class APIConfig(Config):
    auth: AuthConfig
    email: EmailConfig

    @classmethod
    def from_base(cls, auth: AuthConfig, base: Config, email: EmailConfig):
        return cls(
            db=base.db,
            redis=base.redis,
            auth=auth,
            email=email
        )
