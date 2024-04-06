import pytest_asyncio
from dishka.integrations.fastapi import setup_dishka
from httpx import AsyncClient

from swapmaster.main.web import create_app


@pytest_asyncio.fixture(scope="session")
async def client(mock_container):
    app = create_app()
    setup_dishka(mock_container, app)
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
