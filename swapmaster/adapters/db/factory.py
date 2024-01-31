from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine

from swapmaster.adapters.db.config import DBConfig


def create_engine(url: str):
    return create_async_engine(url)


def create_session_maker(engine: AsyncEngine):
    return async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=True)


def create_pool(db_config: DBConfig) -> async_sessionmaker[AsyncSession]:
    engine = create_engine(url=db_config.uri)
    return create_session_maker(engine)
