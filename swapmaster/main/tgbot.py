from swapmaster.common.config.parser import logging_setup
from swapmaster.main.web import get_paths_common
from swapmaster.presentation.tgbot.routers import setup_routers
from swapmaster.presentation.tgbot.config.parser.main import get_bot_config
from swapmaster.presentation.tgbot.factory import create_bot, create_dispatcher


def run_bot():
    paths = get_paths_common()
    config = get_bot_config(paths=paths)
    logging_setup(paths)

    main_bot = create_bot(config.tgbot)
    dispatcher = create_dispatcher()

    setup_routers(dp=dispatcher)


if __name__ == "__main__":
    run_bot()