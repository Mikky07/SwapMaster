import logging

from aiogram import Dispatcher

from .user import setup_user_handlers


logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher):
    routers = [
        setup_user_handlers()
    ]

    for router in routers:
        dp.include_router(router)

    logger.info("tgbot routers set up successfully!")
