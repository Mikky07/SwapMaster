import asyncio
import logging

from aiohttp import web
from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from swapmaster.common.config.parser import logging_setup
from swapmaster.main.web import get_paths_common
from swapmaster.main.di import setup_bot_di
from swapmaster.presentation.tgbot.config.models.webhook import WebhookConfig
from swapmaster.presentation.tgbot.config.parser.main import get_bot_config
from swapmaster.presentation.tgbot.factory import create_bot
from swapmaster.presentation.tgbot.handlers import setup_handlers

logger = logging.getLogger(__name__)


def get_on_startup(bot: Bot, config_: WebhookConfig):
    async def on_startup() -> None:
        await bot.set_webhook(
            config_.url, secret_token=config_.secret
        )

    return on_startup


def run_web_application(dp: Dispatcher, bot: Bot, config_: WebhookConfig):
    app = web.Application()

    webhook_request_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=config_.secret
    )
    webhook_request_handler.register(app, path=config_.path)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=config_.host, port=config_.port)


async def start(bot: Bot, dp: Dispatcher):
    await bot.delete_webhook()
    await dp.start_polling(bot)


def main():
    paths = get_paths_common()
    config = get_bot_config(paths=paths)
    logging_setup(paths)

    dispatcher = Dispatcher()
    bot = create_bot(config)

    setup_dialogs(dispatcher)
    setup_handlers(dp=dispatcher)
    setup_bot_di(
        dp=dispatcher,
        bot_config=config,
    )
    # dispatcher.startup.register(
    #     get_on_startup(
    #         bot=bot,
    #         config_=config.webhook,
    #     )
    # )
    # run_web_application(
    #     dp=dispatcher,
    #     bot=bot,
    #     config_=config.webhook
    # )
    asyncio.run(start(bot, dispatcher))


if __name__ == "__main__":
    main()
