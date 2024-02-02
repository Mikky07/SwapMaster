import logging
from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, Body
from starlette import status

from swapmaster.application.create_commission import NewCommissionDTO, AddCommission
from swapmaster.core.models import Commission
from swapmaster.presentation.api import models

logger = logging.getLogger(__name__)


async def add_commission(
    commission: Annotated[models.Commission, Body(embed=True)],
    interactor: AddCommission = Depends(),
) -> Commission:
    commission_dto: NewCommissionDTO = commission.to_dto()
    new_commission = await interactor(data=commission_dto)
    return new_commission


def setup_commission() -> APIRouter:
    commission_router = APIRouter(prefix="/commission")
    commission_router.add_api_route(path="/new", endpoint=add_commission, methods=["POST"])

    return commission_router
