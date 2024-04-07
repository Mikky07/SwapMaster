import logging
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi import Response
from fastapi.security import OAuth2PasswordRequestForm

from swapmaster.application.common.gateways import UserReader
from swapmaster.presentation.web_api.auth import AuthHandler

logger = logging.getLogger(__name__)


async def login(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_reader: FromDishka[UserReader],
        auth_handler: FromDishka[AuthHandler]
):
    token = await auth_handler.auth(
        username=form_data.username,
        password=form_data.password,
        user_reader=user_reader
    )
    response.set_cookie(
        "Authorization",
        httponly=True,
        value=f"{token.token_type} {token.access_token}"
    )
    return {"success": True}


def setup_auth() -> APIRouter:
    auth_router = APIRouter(prefix="/auth", route_class=DishkaRoute)
    auth_router.add_api_route("/token", endpoint=login, methods=["POST"])
    return auth_router
