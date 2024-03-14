import logging

from aiohttp import web
from aiogram import Dispatcher, Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from swapmaster.common.config.parser import logging_setup
from swapmaster.main.web import get_paths_common
from swapmaster.presentation.tgbot.config.models.webhook import WebhookConfig
from swapmaster.presentation.tgbot.config.parser.main import get_bot_config
from swapmaster.presentation.tgbot.factory import create_bot, create_dispatcher
from swapmaster.presentation.tgbot.handlers import setup_handlers

logger = logging.getLogger(__name__)


def on_startup(bot: Bot, config_: WebhookConfig):
    async def set_webhook() -> None:
        await bot.set_webhook(
            config_.url, secret_token=config_.secret
        )

    return set_webhook


def run_web_application(dp: Dispatcher, bot: Bot, config_: WebhookConfig):
    app = web.Application()

    webhook_request_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=config_.secret
    )
    webhook_request_handler.register(app, path=config_.path)

    dp.startup.register(on_startup(bot=bot, config_=config_))

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=config_.host, port=config_.port)


def main():
    paths = get_paths_common()
    config = get_bot_config(paths=paths)
    logging_setup(paths)

    dispatcher = create_dispatcher()
    bot = create_bot(config)

    setup_handlers(dp=dispatcher)
    run_web_application(
        dp=dispatcher,
        bot=bot,
        config_=config.webhook
    )


if __name__ == "__main__":
    main()
