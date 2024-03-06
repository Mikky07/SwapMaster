import logging

from apscheduler import Scheduler, AsyncScheduler


logger = logging.getLogger(__name__)


def create_sync_scheduler() -> Scheduler:
    scheduler = Scheduler(logger=logger)
    logger.info("sync scheduler set up successfully")
    return scheduler


async def create_async_scheduler() -> AsyncScheduler:
    logger.info("async scheduler set up successfully")
    scheduler_async = AsyncScheduler(logger=logger)
    return scheduler_async
