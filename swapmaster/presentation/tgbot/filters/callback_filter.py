from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class CallbackDataFilter(BaseFilter):
    def __init__(self, callback_data: str):
        self.callback_data = callback_data

    async def __call__(self, callback: CallbackQuery):
        return callback.data == self.callback_data
