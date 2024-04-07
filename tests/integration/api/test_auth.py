from unittest.mock import Mock

import pytest
from httpx import AsyncClient
from starlette.responses import Response


@pytest.mark.asyncio
async def test_auth(client: AsyncClient, auth_handler: Mock):
    response: Response = await client.post(
        '/auth/token',
        data={
            'username': "test_username",
            'password': 'test_password'
        }
    )

    assert response.status_code == 200
    assert auth_handler.auth.called
