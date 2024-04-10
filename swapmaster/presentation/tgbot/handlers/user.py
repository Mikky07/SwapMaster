from aiogram import Router
from aiogram.types import Message
from dishka import FromDishka

from swapmaster.core.models import User
from swapmaster.presentation.tgbot.keyboards import start_menu_keyboard


async def handle_start(message: Message, user: FromDishka[User]):
    await message.answer(
        f"Hello, {user.username}!😁\n"
        f"You`re in SwapMaster main menu!\n"
        f"Please lead following actions:",
        reply_markup=start_menu_keyboard()
    )


def setup_user_handlers() -> Router:
    user_router = Router(name="user_router")
    user_router.message.register(
        callback=handle_start,
    )
    return user_router
