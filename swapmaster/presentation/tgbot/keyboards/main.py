from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text='Create order', callback_data='create_order'),
            InlineKeyboardButton(text='Profile', callback_data='profile')
        ]]
    )
