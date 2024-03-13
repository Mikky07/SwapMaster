from ..models.commission import Commission
from swapmaster.core.utils.exceptions import CommissionIsNotValid


class CommissionService:
    def is_commission_valid(self, value: float) -> bool:
        return 0 <= value <= 100

    def create_commission(
            self,
            value: float
    ) -> Commission:
        if not self.is_commission_valid(value):
            raise CommissionIsNotValid("Commission is not valid!")
        return Commission(id=None, value=value)
