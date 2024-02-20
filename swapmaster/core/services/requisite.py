from swapmaster.core.models import Requisite, PairId


class RequisiteService:
    def create_requisite(
            self,
            name: str,
            pair_id: PairId,
            regular_expression: str
    ) -> Requisite:
        return Requisite(
            id=None,
            name=name,
            pair_id=pair_id,
            regular_expression=regular_expression
        )
