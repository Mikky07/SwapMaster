from dataclasses import dataclass

from swapmaster.adapters.mq.verification.config import EmailConfig
from swapmaster.common.config.models import Config
from swapmaster.presentation.api.config.models.auth import AuthConfig


@dataclass
class APIConfig(Config):
    auth: AuthConfig
    email: EmailConfig
