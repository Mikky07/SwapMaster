import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from swapmaster.application import Authenticate
from swapmaster.application.authenticate import NewUserDTO
from swapmaster.application.common.db import UserUpdater
from swapmaster.application.verifier import Verifier
from swapmaster.core.models import User
from swapmaster.core.utils.exceptions import SMError
from swapmaster.presentation.api.depends.stub import Stub
from swapmaster.core.constants import VerificationStatusEnum


logger = logging.getLogger(__name__)


async def register(
    data: NewUserDTO,
    authenticator: Authenticate = Depends()
):
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
        user_updater: UserUpdater = Depends(Stub(UserUpdater)),
        user: User = Depends(Stub(User)),
        verifier: Verifier = Depends()
) -> User:
    if user.verification_status == VerificationStatusEnum.VERIFIED:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="User already verified"
        )
    try:
        user_verified = await verifier.finish_verification(
            user=user,
            verification_code=verification_code,
            user_updater=user_updater
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
