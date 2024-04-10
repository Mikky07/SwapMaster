import operator
from typing import Any

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Select, Column, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from dishka import FromDishka

from swapmaster.application.common.gateways import CurrencyListReader
from swapmaster.core.models import Currency
from swapmaster.presentation.tgbot.keyboards.main import OrderCallbackData
from swapmaster.presentation.tgbot.states import OrderState


async def start_order_creating(
        callback: CallbackQuery,
        currency_gateway: FromDishka[CurrencyListReader],
        dialog_manager: DialogManager
):
    currencies: list[Currency] = await currency_gateway.get_currency_list()
    await dialog_manager.start(
        state=OrderState.currency_to
    )
    dialog_manager.dialog_data['currencies'] = currencies


async def handle_currency_choose(
        callback: CallbackQuery, widget: Any,
        manager: DialogManager, item_id: str
):
    print(item_id)


def currency_id_getter(currency: Currency) -> str:
    return str(currency.id)


order_dialog = Dialog(
    Window(
        Const("Choose the currency that you want to receive:"),
        Column(
            Select(
                Format("📍 {item.name}"),
                id="currencies",
                items=F['dialog_data']['currencies'],
                item_id_getter=currency_id_getter,
                on_click=handle_currency_choose
            ),
        ),
        state=OrderState.currency_to,
    ),
)


def setup_order_handlers() -> Router:
    order_router = Router(name='order_router')
    order_router.callback_query.register(start_order_creating, OrderCallbackData.filter())
    return order_router
