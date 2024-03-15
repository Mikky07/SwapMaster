import logging

from aiogram import Dispatcher

from swapmaster.main.ioc import IoC
from .ioc_middleware import IoCMiddleware

logger = logging.getLogger(__name__)


def setup_middlewares(dp: Dispatcher, ioc: IoC):
    dp.update.outer_middleware(
        IoCMiddleware(ioc=ioc)
    )

    logger.info("middlewares set up successfully!")
