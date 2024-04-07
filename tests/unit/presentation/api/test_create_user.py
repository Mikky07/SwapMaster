import pytest
from httpx import AsyncClient

from tests.mocks.interactors.user import CreateUserMock


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, user_creator: CreateUserMock):
    response = await client.post(
        "/users/",
        json={
            "username": "test_username",
            "email": "test@email.ru",
            "password": "test_password"
        }
    )

    assert response.status_code == 200
    assert user_creator.called
