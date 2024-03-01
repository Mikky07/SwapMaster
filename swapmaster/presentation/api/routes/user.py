import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from swapmaster.application import Authenticate
from swapmaster.application.authenticate import NewUserDTO
from swapmaster.application.verifier import Verifier
from swapmaster.core.models import User
from swapmaster.core.utils.exceptions import SMError
from swapmaster.presentation.api.depends.stub import Stub


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
        user=Depends(Stub(User)),
):
    logger.info(verification_code)
    logger.info(user.id)


def setup_user() -> APIRouter:
    user_router = APIRouter(prefix="/users")
    user_router.add_api_route("/", endpoint=register, methods=["POST"])
    user_router.add_api_route('/verify-account/{verification_code}', endpoint=verify_account, methods=["GET"])
    return user_router
