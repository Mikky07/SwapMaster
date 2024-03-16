from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Depends

from swapmaster.application.common.db.currency_gateway import CurrencyListReader
from swapmaster.presentation.web_api.depends.stub import Stub
from swapmaster.core.models import Currency


async def add_currency():
    ...


async def get_all_currencies(
        currency_db: Annotated[CurrencyListReader, Depends(Stub(CurrencyListReader))]
) -> list[Currency]:
    currencies = await currency_db.get_currency_list()
    return currencies


def setup_currency() -> APIRouter:
    currency_router = APIRouter(prefix="/currencies")
    currency_router.add_api_route(path="", endpoint=get_all_currencies, methods=["GET"])

    return currency_router
