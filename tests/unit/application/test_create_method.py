import pytest

from swapmaster.application.create_method import CreateMethod, NewMethodDTO
from swapmaster.core.models import CurrencyId, MethodId
from tests.mocks import UoWMock, MethodGatewayMock


TEST_METHOD_NAME = "method1"
TEST_METHOD_CURRENCY_ID = CurrencyId(1)


@pytest.mark.asyncio
async def test_create_method_(
        uow: UoWMock,
        method_gateway: MethodGatewayMock
):
    new_method = NewMethodDTO(
        name=TEST_METHOD_NAME,
        currency_id=TEST_METHOD_CURRENCY_ID
    )

    method_creator = CreateMethod(
        method_gateway=method_gateway,
        uow=uow
    )

    created_method = await method_creator(data=new_method)

    assert type(created_method.id) is MethodId
    assert created_method.name == TEST_METHOD_NAME
    assert created_method.currency_id == TEST_METHOD_CURRENCY_ID

    assert uow.committed
