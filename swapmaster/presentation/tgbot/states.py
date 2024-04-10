from aiogram.filters.state import StatesGroup, State


class OrderState(StatesGroup):
    currency_to = State()
    method_to = State()
