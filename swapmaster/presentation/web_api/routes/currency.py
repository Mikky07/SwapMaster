from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi.routing import APIRouter

from swapmaster.application.common.gateways.currency_gateway import CurrencyListReader
from swapmaster.core.models import Currency


async def add_currency():
    ...


async def get_all_currencies(
        currency_gateway: FromDishka[CurrencyListReader]
) -> list[Currency]:
    currencies = await currency_gateway.get_currency_list()
    return currencies


def setup_currency() -> APIRouter:
    currency_router = APIRouter(prefix="/currencies", route_class=DishkaRoute)
    currency_router.add_api_route(path="", endpoint=get_all_currencies, methods=["GET"])

    return currency_router
