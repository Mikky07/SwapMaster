from aiogram import Router
from aiogram.filters import CommandStart
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format, Const

from swapmaster.presentation.tgbot.states import OrderSG, MainSG

user_dialog = Dialog(
    Window(
        Format(
            "Hello, {event.from_user.username}!😁\n"
            "You`re in SwapMaster main menu!\n"
            "Please lead following actions:"
        ),
        Start(Const("Orders"), state=OrderSG.main, id="create_order"),
        state=MainSG.main,
    )
)


async def handle_start(_, dialog_manager: DialogManager):
    await dialog_manager.start(state=MainSG.main)


def setup_user_handlers() -> Router:
    user_router = Router(name="user_router")
    user_router.message.register(
        handle_start,
        CommandStart()
    )
    return user_router
