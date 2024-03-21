from dataclasses import dataclass

from swapmaster.application.common.interactor import Interactor
from swapmaster.core.models.commission import Commission
from swapmaster.core.services.commission import CommissionService
from swapmaster.core.utils.exceptions import AlreadyExists
from swapmaster.application.common.db.commission_gateway import CommissionWriter
from swapmaster.application.common import UoW


@dataclass
class NewCommissionDTO:
    value: float


class CreateCommission(Interactor):
    def __init__(
        self,
        commission_gateway: CommissionWriter,
        commission_service: CommissionService,
        uow: UoW
    ):
        self.commission_gateway = commission_gateway
        self.commission_service = commission_service
        self.uow = uow

    async def __call__(self, data: NewCommissionDTO) -> Commission:
        new_commission = self.commission_service.create_commission(
            value=data.value
        )
        is_commission_exists = await self.commission_gateway.is_commission_exists(
            commission=new_commission
        )
        if is_commission_exists:
            raise AlreadyExists(text="commission with this value already exists")
        saved_commission: Commission = await self.commission_gateway.add_commission(
            commission=new_commission
        )
        await self.uow.commit()
        return saved_commission
