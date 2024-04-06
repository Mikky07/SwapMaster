import logging

from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from swapmaster.core.utils.exceptions import SMError, AuthFailed


logger = logging.getLogger(__name__)


async def exception_handler(request, exc: SMError):
    response = JSONResponse(content={"message": str(exc)})
    match exc:
        case AuthFailed():
            response.status_code = status.HTTP_401_UNAUTHORIZED
        case _:
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
    return response


def setup_exception_handler(app: FastAPI):
    app.add_exception_handler(SMError, handler=exception_handler)

    logger.info("Exceptions set up successfully!")
