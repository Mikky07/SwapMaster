import logging
from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from starlette import status

from swapmaster.application.create_commission import NewCommissionDTO
from swapmaster.core.models import Commission
from swapmaster.core.utils import exceptions
from swapmaster.presentation.api import models
from swapmaster.presentation.api.depends.stub import Stub
from swapmaster.presentation.interactor_factory import InteractorFactory

logger = logging.getLogger(__name__)


async def add_commission(
    commission: models.Commission,
    ioc: Annotated[InteractorFactory, Depends(Stub(InteractorFactory))]
) -> Commission:
    commission_dto: NewCommissionDTO = commission.to_dto()
    async with ioc.commission_creator() as create_commission:
        try:
            new_commission = await create_commission(data=commission_dto)
        except exceptions.AlreadyExists as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=str(e)
            )
    return new_commission


async def get_commissions() -> list[Commission]:
    ...


def setup_commission() -> APIRouter:
    commission_router = APIRouter(prefix="/commissions")
    commission_router.add_api_route(path="", endpoint=add_commission, methods=["POST"])

    return commission_router
