import logging
from contextlib import asynccontextmanager

from apscheduler import Scheduler, AsyncScheduler


logger = logging.getLogger(__name__)


def create_sync_scheduler() -> Scheduler:
    scheduler = Scheduler(logger=logger)
    logger.info("sync scheduler set up successfully")
    return scheduler


def create_async_scheduler() -> AsyncScheduler:
    logger.info("async scheduler set up successfully")
    scheduler_async = AsyncScheduler(logger=logger)
    return scheduler_async


@asynccontextmanager
async def async_scheduler_startup_handler(scheduler: AsyncScheduler) -> None:
    async with scheduler:
        yield

