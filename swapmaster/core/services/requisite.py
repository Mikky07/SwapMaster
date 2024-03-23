import re

from swapmaster.core.models import Requisite, OrderRequisite


class RequisiteService:
    def check_requisites_validity(
            self,
            pair_requisites: list[Requisite],
            order_requisites: list[OrderRequisite]
    ) -> bool:
        requisites_required = pair_requisites.copy()
        requisites_filled = order_requisites.copy()

        if len(requisites_required) != len(requisites_filled):
            return False

        requisites_filled_ids = set(r.requisite_id for r in requisites_filled)

        for requisite_required in requisites_required:
            if requisite_required.id not in requisites_filled_ids:
                return False

            for requisite_filled in requisites_filled:
                if requisite_filled.requisite_id == requisite_required.id:
                    pattern = requisite_required.regular_expression
                    if not re.fullmatch(pattern=pattern, string=requisite_filled.data):
                        return False
                    requisites_filled.remove(requisite_filled)
                    break

        return True
