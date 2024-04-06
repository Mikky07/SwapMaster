from typing import Dict

from swapmaster.application.common.gateways.method_gateway import (
    MethodWriter,
    MethodReader
)
from swapmaster.core.models import MethodId, Method, CurrencyId


class MethodGatewayMock(MethodWriter, MethodReader):
    def __init__(self):
        self.methods: Dict[MethodId, Method] = {}

    async def is_method_available(self, name: str, currency_id: CurrencyId) -> bool:
        for method in self.methods.values():
            if method.name == name and method.currency_id == currency_id:
                return True
        return False

    async def get_method_by_id(self, method_id: MethodId) -> Method:
        return self.methods[method_id]

    async def add_method(self, method: Method) -> Method:
        max_of_ids = max(self.methods) if self.methods else 0
        new_method_id = max_of_ids + 1
        method.id = new_method_id
        self.methods[method.id] = method
        return self.methods.get(method.id)

    async def get_method_list(self) -> list[Method]:
        return list(self.methods.values())
