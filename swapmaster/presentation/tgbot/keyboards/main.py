from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class OrderCallbackData(CallbackData, prefix='order'):
    intention: str


def start_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Create order", callback_data=OrderCallbackData(intention="create").pack())
    return builder.as_markup()
