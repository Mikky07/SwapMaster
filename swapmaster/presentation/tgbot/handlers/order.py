from typing import Any

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Column, SwitchTo, Row, Start
from aiogram_dialog.widgets.text import Const, Format
from dishka import AsyncContainer
from dishka.integrations.aiogram import CONTAINER_NAME

from swapmaster.application.common.gateways import CurrencyListReader, MethodReader
from swapmaster.application.get_available_transfer_info import GetAvailableTransferInformation
from swapmaster.core.models import Currency, CurrencyId, Method, MethodId
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
    container = dialog_manager.middleware_data[CONTAINER_NAME]
    available_transfer_information_fetcher = await container.get(GetAvailableTransferInformation)
    available_transfer_methods = await available_transfer_information_fetcher(MethodId(item_id))
    dialog_manager.dialog_data['transfer_methods'] = available_transfer_methods
    dialog_manager.dialog_data['method'] = item_id
    await dialog_manager.next()


async def handle_transfer_method_choose(
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
        Const("Choose network or bank:"),
        Column(
            Select(
                Format("{item.name}"),
                id="methods",
                items=F["dialog_data"]["methods"],
                item_id_getter=method_id_getter,
                on_click=handle_method_choose
            )
        ),
        OrderMenuButton,
        state=OrderSG.method_to
    ),
    Window(
        Const("Choose method for payment:"),
        Column(
            Select(
                Format("Method: {item.method_from.name} Course: {item.course_value}"),
                id="methods_for_payment",
                items=F["dialog_data"]["transfer_methods"],
                item_id_getter=lambda m: str(m.pair_id),
                on_click=handle_transfer_method_choose
            )
        ),
        OrderMenuButton,
        state=OrderSG.method_from
    ),
)
