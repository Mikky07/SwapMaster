import logging

from aiohttp import web
from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from apscheduler import AsyncScheduler

from swapmaster.adapters.mq import create_async_scheduler, create_sync_scheduler, async_scheduler_startup_handler
from swapmaster.common.config.parser import logging_setup
from swapmaster.main.web import get_paths_common
from swapmaster.main.di import setup_bot_di
from swapmaster.presentation.tgbot.config.models.webhook import WebhookConfig
from swapmaster.presentation.tgbot.config.parser.main import get_bot_config
from swapmaster.presentation.tgbot.factory import create_bot
from swapmaster.presentation.tgbot.handlers import setup_handlers

logger = logging.getLogger(__name__)


def get_on_startup(bot: Bot, config_: WebhookConfig, scheduler_async: AsyncScheduler):
    async def on_startup() -> None:
        await bot.set_webhook(
            config_.url, secret_token=config_.secret
        )
        async with async_scheduler_startup_handler(scheduler=scheduler_async):
            yield

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


def main():
    paths = get_paths_common()
    config = get_bot_config(paths=paths)
    logging_setup(paths)

    dispatcher = Dispatcher()
    bot = create_bot(config)

    scheduler_async = create_async_scheduler()
    scheduler_sync = create_sync_scheduler()

    setup_dialogs(dispatcher)
    setup_handlers(dp=dispatcher)
    setup_bot_di(
        dp=dispatcher,
        bot_config=config,
        scheduler_sync=scheduler_sync,
        scheduler_async=scheduler_async
    )
    dispatcher.startup.register(
        get_on_startup(
            bot=bot,
            config_=config.webhook,
            scheduler_async=scheduler_async
        )
    )
    run_web_application(
        dp=dispatcher,
        bot=bot,
        config_=config.webhook
    )


if __name__ == "__main__":
    main()
