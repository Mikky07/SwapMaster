from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from swapmaster.application import Authenticate
from swapmaster.application.authenticate import NewUserDTO
from swapmaster.core.utils.exceptions import SMError


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


def setup_user() -> APIRouter:
    user_router = APIRouter(prefix="/users")
    user_router.add_api_route("/", endpoint=register, methods=["POST"])
    return user_router
