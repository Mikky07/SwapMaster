import pytest
from httpx import AsyncClient

from tests.mocks.interactors.user import CreateUserMock


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, user_creator: CreateUserMock):
    test_username = "test_username"
    test_email = "test@email.ru"
    test_password = "test_password"

    response = await client.post(
        "/users/",
        data={
            "username": test_username,
            "email": test_email,
            "password": test_password
        }
    )

    assert response.status_code == 200
    assert user_creator.called

    print(response)
