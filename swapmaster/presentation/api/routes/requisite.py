from fastapi import APIRouter, Depends

from swapmaster.application.create_requisite import NewRequisiteDTO, AddRequisite


async def add_requisite(
        data: NewRequisiteDTO,
        interactor: AddRequisite = Depends()
):
    await interactor(data=data)


def setup_requisite() -> APIRouter:
    requisite_router = APIRouter(prefix="/requisites")
    requisite_router.add_api_route("", endpoint=add_requisite, methods=["POST"])
    return requisite_router
