from swapmaster.core.services import RequisiteService


class RequisiteServiceMock(RequisiteService):
    """We can transfer values that BL functions will return to check all cases simply"""
    def __init__(self):
        self.requisites_valid: bool = True

    def check_requisites_validity(self, *args, **kwargs) -> bool:
        return self.requisites_valid