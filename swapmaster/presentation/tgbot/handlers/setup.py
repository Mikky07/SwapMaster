import logging

from aiogram import Dispatcher

from .order import setup_order_handlers, order_dialog
from .user import setup_user_handlers


logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher):
    routers = [
        setup_user_handlers(),
        setup_order_handlers(),
        order_dialog
    ]

    for router in routers:
        dp.include_router(router)

    logger.info("tgbot routers set up successfully!")
