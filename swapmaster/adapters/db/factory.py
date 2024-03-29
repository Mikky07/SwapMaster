from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine

from swapmaster.adapters.db.config import DBConfig
from swapmaster.adapters.db.config.models import RedisConfig


def create_engine(url: str):
    return create_async_engine(url)


def create_session_maker(engine: AsyncEngine):
    return async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=True)


def create_pool(db_config: DBConfig) -> async_sessionmaker[AsyncSession]:
    engine = create_engine(url=db_config.url)
    return create_session_maker(engine)


def create_redis(redis_config: RedisConfig) -> Redis:
    return Redis(host=redis_config.host, port=redis_config.port)
