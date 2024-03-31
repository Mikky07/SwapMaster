from aiogram.filters.state import StatesGroup, State


class OrderState(StatesGroup):
    method_from = State()
    method_to = State()
