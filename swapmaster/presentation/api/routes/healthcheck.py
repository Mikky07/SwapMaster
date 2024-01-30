from dataclasses import dataclass

from fastapi.routing import APIRouter
from starlette.status import HTTP_200_OK


@dataclass
class OkStatus:
    ok = True


async def healthcheck():
    status = OkStatus()
    if status.ok:
        return HTTP_200_OK


def healthcheck_setup() -> APIRouter:
    healthcheck_router = APIRouter(prefix='/healthcheck')
    healthcheck_router.add_api_route(path='/', endpoint=healthcheck, methods=["GET"])
    return healthcheck_router
