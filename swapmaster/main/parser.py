import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from swapmaster.adapters.db.config import load_db_config
from swapmaster.adapters.db.factory import create_pool
from swapmaster.adapters.db.gateways.sqlalchemy import ReserveGateway
from swapmaster.application.reserve_refresh import ReserveRefresh
from swapmaster.adapters.remote_wallets.reserve_obtaining import ReserveObtainer
from swapmaster.main.db_uow import UowAsyncSession
from swapmaster.common.config.models import Paths
from swapmaster.common.config.parser import read_config, get_paths


def get_paths_common() -> Paths:
    return get_paths("")


# stub
async def refresh(pool: async_sessionmaker[AsyncSession]):
    async with pool() as session:
        reserve_gateway = ReserveGateway(session=session)
        reserve_size_obtainer = ReserveObtainer()
        uow = UowAsyncSession(session=session)
        reserve_refresh = ReserveRefresh(
            uow=uow,
            reserve_reader=reserve_gateway,
            reserve_updater=reserve_gateway,
            reserve_size_obtainer=reserve_size_obtainer
        )
        await reserve_refresh()


async def parse(pool: async_sessionmaker[AsyncSession]):
    ...


async def main():
    paths = get_paths_common()
    config_dct = read_config(paths)
    db_config = load_db_config(config_dct.get("db"))
    pool = create_pool(db_config)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(refresh, args=[pool], trigger="interval", seconds=10)
    scheduler.start()

if __name__ == "__main__":
    asyncio.run(main())
