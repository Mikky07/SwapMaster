import logging

from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware

logger = logging.getLogger(__name__)


def setup_middlewares(dp: Dispatcher):
    # dp.callback_query.middleware(ThrottlingMiddleware())
    logger.info("middlewares set up successfully!")
