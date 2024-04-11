from aiogram.filters.state import StatesGroup, State


class OrderSG(StatesGroup):
    main = State()
    currency_to = State()
    method_to = State()
    method_from = State()


class MainSG(StatesGroup):
    main = State()
