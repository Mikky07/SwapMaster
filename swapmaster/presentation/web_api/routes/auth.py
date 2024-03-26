import logging
from typing import Annotated

from starlette import status
from fastapi import APIRouter, Depends
from fastapi import Response
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from swapmaster.application.common.gateways import UserReader
from swapmaster.core.utils.exceptions import SMError
from swapmaster.presentation.web_api.depends.auth import AuthProvider
from swapmaster.presentation.web_api.depends.stub import Stub

logger = logging.getLogger(__name__)


async def login(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_provider: Annotated[AuthProvider, Depends(Stub(AuthProvider))],
        user_reader: Annotated[UserReader, Depends(Stub(UserReader))]
):
    try:
        token = await auth_provider.auth(form_data=form_data, user_reader=user_reader)
    except SMError as s:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=s.text
        )
    response.set_cookie(
        "Authorization",
        httponly=True,
        value=f"{token.token_type} {token.access_token}"
    )
    return {"success": True}


def setup_auth() -> APIRouter:
    auth_router = APIRouter(prefix="/auth")
    auth_router.add_api_route("/token", endpoint=login, methods=["POST"])
    return auth_router
