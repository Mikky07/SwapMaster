from fastapi.routing import APIRouter
from fastapi import Depends

from swapmaster.adapters.db.currency_db import CurrencyGateway
from swapmaster.presentation.api.depends.stub import Stub
from swapmaster.core.models import dto


async def get_all_currencies(currency_db: CurrencyGateway = Depends(Stub(CurrencyGateway))) -> list[dto.Currency]:
    return await currency_db.get_currency_list()


def setup_currency() -> APIRouter:
    currency_router = APIRouter(prefix="/currency")
    currency_router.add_api_route(path="/all", endpoint=get_all_currencies, methods=["GET"])

    return currency_router
