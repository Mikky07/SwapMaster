import logging

from aiogram import Dispatcher

from .order import order_dialog
from .user import setup_user_handlers, user_dialog


logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher):
    routers = [
        setup_user_handlers(),
        order_dialog,
        user_dialog
    ]

    for router in routers:
        dp.include_router(router)

    logger.info("tgbot routers set up successfully!")
