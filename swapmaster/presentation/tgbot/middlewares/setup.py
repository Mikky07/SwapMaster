import logging

from aiogram import Dispatcher

from swapmaster.presentation.interactor_factory import InteractorFactory
from .ioc_middleware import IoCMiddleware

logger = logging.getLogger(__name__)


def setup_middlewares(dp: Dispatcher, ioc: InteractorFactory):
    dp.update.middleware.register(IoCMiddleware(ioc=ioc))

    logger.info("middlewares set up successfully!")
