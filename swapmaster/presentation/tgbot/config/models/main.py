from dataclasses import dataclass

from swapmaster.common.config.models import Config
from swapmaster.presentation.tgbot.config.models.tgbot import TGBotConfig


@dataclass
class BotConfig(Config):
    tgbot: TGBotConfig

    @classmethod
    def from_base(cls, base: Config, tgbot: TGBotConfig):
        return cls(
            db=base.db,
            redis=base.redis,
            central=base.central,
            tgbot=tgbot
        )
