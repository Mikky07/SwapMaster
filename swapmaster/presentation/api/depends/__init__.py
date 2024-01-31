import logging

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from swapmaster.adapters.db.currency_db import CurrencyGateway
from .currency import CurrencyDBProvider

logger = logging.getLogger(__name__)


def setup_dependencies(app: FastAPI, pool: async_sessionmaker[AsyncSession]):
    currency_provider = CurrencyDBProvider(pool=pool)

    app.dependency_overrides[CurrencyGateway] = currency_provider.get_currency_db

    logger.info("dependencies set up!")
