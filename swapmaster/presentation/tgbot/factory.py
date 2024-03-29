import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from swapmaster.presentation.tgbot.config.models.main import BotConfig


logger = logging.getLogger(__name__)


def create_dispatcher() -> Dispatcher:
    return Dispatcher()


def create_bot(config: BotConfig) -> Bot:
    main_bot = Bot(
        token=config.tgbot.token,
        parse_mode=ParseMode.HTML
    )

    return main_bot
