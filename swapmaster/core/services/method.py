from ..models.method import Method
from ..models.currency import CurrencyId


class MethodService:
    def create_method(
        self,
        name: str,
        currency_id: CurrencyId
    ) -> Method:
        return Method(
            method_id=None,
            name=name,
            currency_id=currency_id,
            reserve=None
        )
