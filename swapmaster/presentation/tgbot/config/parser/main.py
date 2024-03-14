from swapmaster.common.config.models import Paths
from swapmaster.common.config.parser import read_config, load_config
from swapmaster.presentation.tgbot.config.models.main import BotConfig
from swapmaster.presentation.tgbot.config.parser.tgbot import load_tgbot_config
from swapmaster.presentation.tgbot.config.parser.webhook import load_webhook_config


def get_bot_config(paths: Paths) -> BotConfig:
    config_dict = read_config(paths=paths)
    return BotConfig.from_base(
        tgbot=load_tgbot_config(config_dict.get("bot")),
        base=load_config(config_dict),
        webhook=load_webhook_config(config_dict.get("bot-webhook"))
    )
