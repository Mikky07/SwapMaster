from dataclasses import dataclass

from swapmaster.common.config.models import Config
from swapmaster.presentation.tgbot.config.models.tgbot import TGBotConfig
from swapmaster.presentation.tgbot.config.models.webhook import WebhookConfig


@dataclass
class BotConfig(Config):
    tgbot: TGBotConfig
    webhook: WebhookConfig

    @classmethod
    def from_base(cls, base: Config, tgbot: TGBotConfig, webhook: WebhookConfig):
        return cls(
            db=base.db,
            redis=base.redis,
            central=base.central,
            tgbot=tgbot,
            webhook=webhook
        )
