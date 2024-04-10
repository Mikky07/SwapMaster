from typing import Any

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Column, SwitchTo, Row, Start
from aiogram_dialog.widgets.text import Const, Format
from dishka import AsyncContainer
from dishka.integrations.aiogram import CONTAINER_NAME

from swapmaster.application.common.gateways import CurrencyListReader, MethodReader
from swapmaster.core.models import Currency, CurrencyId, Method
from swapmaster.presentation.tgbot.states import OrderSG, MainSG


async def load_currencies(
        _callback: CallbackQuery,
        _widget: Any,
        dialog_manager: DialogManager,
):
    container: AsyncContainer = dialog_manager.middleware_data[CONTAINER_NAME]
    currency_gateway = await container.get(CurrencyListReader)
    currencies: list[Currency] = await currency_gateway.get_currency_list()
    dialog_manager.dialog_data['currencies'] = currencies


async def handle_currency_choose(
        _callback: CallbackQuery,
        _widget: Any,
        dialog_manager: DialogManager,
        item_id: str
):
    container: AsyncContainer = dialog_manager.middleware_data[CONTAINER_NAME]
    method_gateway = await container.get(MethodReader)
    methods = await method_gateway.get_methods_for_currency(currency_id=CurrencyId(item_id))
    dialog_manager.dialog_data['currency'] = item_id
    dialog_manager.dialog_data['methods'] = methods
    await dialog_manager.next()


async def handle_method_choose(
        _callback: CallbackQuery,
        _widget: Any,
        dialog_manager: DialogManager,
        item_id: str
):
    ...


def currency_id_getter(currency: Currency) -> str:
    return str(currency.id)

def method_id_getter(method: Method) -> str:
    return str(method.id)


OrderMenuButton = SwitchTo(id="cancel_order", text=Const("✖️"), state=OrderSG.main)

order_dialog = Dialog(
    Window(
        Const("Choose one of this actions:"),
        Row(
            SwitchTo(
                Const("Create"),
                id="create_order",
                state=OrderSG.currency_to,
                on_click=load_currencies
            ),
            Start(
                id="main_menu",
                state=MainSG.main,
                text=Const("🏘")
            )
        ),
        state=OrderSG.main
    ),
    Window(
        Const("Choose the currency that you want to receive:"),
        Column(
            Select(
                Format("{item.name}"),
                id="currencies",
                items=F['dialog_data']['currencies'],
                item_id_getter=currency_id_getter,
                on_click=handle_currency_choose
            ),
        ),
        OrderMenuButton,
        state=OrderSG.currency_to,
    ),
    Window(
        Const("Choose service, when you have to receive:"),
        Column(
            Select(
                Format("item.name"),
                id="methods",
                items=F["dialog_data"]["methods"],
                item_id_getter=method_id_getter,
                on_click=handle_method_choose
            )
        ),
        state=OrderSG.method_to
    )
)
