from dataclasses import dataclass

from swapmaster.application.common.protocols.method_gateway import MethodWriter
from swapmaster.core.services.method import MethodService
from swapmaster.core.models import Method, CurrencyId
from .common.interactor import Interactor
from .common.uow import UoW


@dataclass
class NewMethodDTO:
    name: str
    currency_id: CurrencyId


class AddMethod(Interactor[NewMethodDTO, Method]):
    def __init__(
            self,
            method_db_gateway: MethodWriter,
            method_service: MethodService,
            uow: UoW
    ):
        self.method_db_gateway = method_db_gateway
        self.method_service = method_service
        self.uow = uow

    async def __call__(self, data: NewMethodDTO) -> Method:
        new_method: Method = self.method_service.create_method(
            name=data.name,
            currency_id=data.currency_id
        )
        method: Method = await self.method_db_gateway.add_method(method=new_method)
        await self.uow.commit()
        return method