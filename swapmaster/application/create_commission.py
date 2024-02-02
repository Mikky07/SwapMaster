from dataclasses import dataclass

from swapmaster.application.common.interactor import Interactor
from swapmaster.core.models.commission import Commission
from swapmaster.core.services.commission import CommissionService
from .common.protocols.commission_gateway import CommissionWriter
from .common.uow import UoW


@dataclass
class NewCommissionDTO:
    value: float


class AddCommission(Interactor[NewCommissionDTO, Commission]):
    def __init__(
            self,
            commission_db_gateway: CommissionWriter,
            commission_service: CommissionService,
            uow: UoW
    ):
        self.commission_db_gateway = commission_db_gateway
        self.commission_service = commission_service
        self.uow = uow

    async def __call__(self, data: NewCommissionDTO) -> Commission:
        new_commission = self.commission_service.create_commission(
            value=data.value
        )
        await self.uow.commit()
        commission: Commission = await self.commission_db_gateway.add_commission(
            commission=new_commission
        )
        return commission
