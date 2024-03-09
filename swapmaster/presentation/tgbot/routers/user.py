from aiogram import Router
from aiogram.types import Message


async def handle_start(message: Message):
    await message.answer("Hello!")


def setup_user_router() -> Router:
    user_router = Router(name="user_router")
    user_router.message.register(
        callback=handle_start,
    )
    return user_router
