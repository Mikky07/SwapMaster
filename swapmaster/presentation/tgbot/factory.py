from aiogram import Bot, Dispatcher

from swapmaster.presentation.tgbot.config.models.tgbot import TGBotConfig


def create_bot(config: TGBotConfig) -> Bot:
    return Bot(
        token=config.token
    )


def create_dispatcher() -> Dispatcher:
    return Dispatcher()
