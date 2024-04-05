import logging

from aiogram import Dispatcher

logger = logging.getLogger(__name__)


def setup_middlewares(dp: Dispatcher):
    logger.info("middlewares set up successfully!")
