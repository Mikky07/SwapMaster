import logging

from aiogram import Dispatcher

from swapmaster.presentation.tgbot import BotInteractorFactory
from .ioc_middleware import IoCMiddleware

logger = logging.getLogger(__name__)


def setup_middlewares(dp: Dispatcher, ioc: BotInteractorFactory):
    dp.update.middleware.register(IoCMiddleware(ioc=ioc))

    logger.info("middlewares set up successfully!")
