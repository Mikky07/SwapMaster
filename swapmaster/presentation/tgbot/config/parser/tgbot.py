from swapmaster.presentation.tgbot.config.models.tgbot import TGBotConfig


def load_tgbot_config(dct: dict) -> TGBotConfig:
    return TGBotConfig(
        token=dct.get("token")
    )
