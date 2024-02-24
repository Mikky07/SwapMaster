from fastapi import APIRouter


async def register(
    interactor
):
    ...


def setup_user() -> APIRouter:
    user_router = APIRouter(prefix="/users")
    user_router.add_api_route("/", endpoint=register, methods=["POST"])
    return user_router
