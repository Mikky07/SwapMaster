import logging

from aiogram import Dispatcher

from .user import setup_user_router


logger = logging.getLogger(__name__)


def setup_routers(dp: Dispatcher):
    routers = [
        setup_user_router()
    ]

    for router in routers:
        dp.include_router(router)

    logger.info("tgbot routers set up successfully!")
