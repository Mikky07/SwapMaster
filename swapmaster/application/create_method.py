from dataclasses import dataclass

from swapmaster.application.common.gateways.method_gateway import MethodWriter
from swapmaster.core.models import Method, CurrencyId
from swapmaster.application.common.interactor import Interactor
from swapmaster.application.common.uow import UoW


@dataclass
class NewMethodDTO:
    name: str
    currency_id: CurrencyId


class CreateMethod(Interactor):
    def __init__(
        self,
        method_gateway: MethodWriter,
        uow: UoW
    ):
        self.method_gateway = method_gateway
        self.uow = uow

    async def __call__(self, data: NewMethodDTO) -> Method:
        new_method = Method(
            id=None,
            reserve=None,
            currency_id=data.currency_id,
            name=data.name
        )

        method: Method = await self.method_gateway.add_method(method=new_method)

        await self.uow.commit()
        return method
