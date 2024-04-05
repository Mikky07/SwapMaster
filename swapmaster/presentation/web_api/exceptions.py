import logging

from fastapi import FastAPI, HTTPException
from starlette import status

from swapmaster.core.utils.exceptions import SMError, AuthFailed


logger = logging.getLogger(__name__)


async def exception_handler(request, exc: SMError):
    match exc:
        case AuthFailed():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exc)
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=str(exc)
            )


def setup_exception_handler(app: FastAPI):
    app.add_exception_handler(SMError, handler=exception_handler)

    logger.info("Exceptions set up successfully!")
