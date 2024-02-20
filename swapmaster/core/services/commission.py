from ..models.commission import Commission


class CommissionService:
    def create_commission(
            self,
            value: float
    ) -> Commission:
        return Commission(id=None, value=value)
