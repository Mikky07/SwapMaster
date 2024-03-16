import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from swapmaster.application.authenticate import NewUserDTO
from swapmaster.core.utils.exceptions import SMError
from swapmaster.core.models import User
from swapmaster.presentation.web_api.depends.stub import Stub
from swapmaster.core.constants import VerificationStatusEnum
from swapmaster.presentation.interactor_factory import InteractorFactory

logger = logging.getLogger(__name__)


async def register(
    data: NewUserDTO,
    ioc: Annotated[InteractorFactory, Depends(Stub(InteractorFactory))]
):
    async with ioc.get_authenticator() as authenticator:
        try:
            registered_user = await authenticator(data=data)
        except SMError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=str(e)
            )
    return registered_user


async def verify_account(
        verification_code: str,
        user: Annotated[User, Depends(Stub(User))],
        ioc: Annotated[InteractorFactory, Depends(Stub(InteractorFactory))]
):
    if user.verification_status == VerificationStatusEnum.VERIFIED:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="User already verified"
        )
    async with ioc.get_verifier() as verifier:
        try:
            user_verified = await verifier.finish_verification(
                verification_code=verification_code
            )
        except SMError as e:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=str(e)
            )
    return user_verified


def setup_user() -> APIRouter:
    user_router = APIRouter(prefix="/users")
    user_router.add_api_route("/", endpoint=register, methods=["POST"])
    user_router.add_api_route('/verify-account/{verification_code}', endpoint=verify_account, methods=["GET"])
    return user_router
