import logging

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from swapmaster.application import WebVerifier
from swapmaster.application.create_user import NewUserDTO, CreateUser
from swapmaster.core.models import User

logger = logging.getLogger(__name__)


async def register(
    data: NewUserDTO,
    user_creator: FromDishka[CreateUser]
):
    registered_user = await user_creator(data=data)
    return registered_user


async def verify_account(
        verification_code: str,
        web_verifier: FromDishka[WebVerifier],
        user: FromDishka[User]
):
    user_verified = await web_verifier.finish_verification(
        verification_code=verification_code,
        user=user
    )
    return user_verified


def setup_user() -> APIRouter:
    user_router = APIRouter(prefix="/users", route_class=DishkaRoute)
    user_router.add_api_route("/", endpoint=register, methods=["POST"])
    user_router.add_api_route('/verify-account/{verification_code}', endpoint=verify_account, methods=["GET"])
    return user_router
