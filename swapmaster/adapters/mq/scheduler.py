from datetime import datetime
from typing import Callable, Any

from apscheduler import AsyncScheduler, Scheduler, RunState
from apscheduler.triggers.date import DateTrigger

from swapmaster.application.common.task_solver import TaskSolver


class TaskSolverImp(TaskSolver):
    def __init__(
            self,
            scheduler_async: AsyncScheduler,
            scheduler_sync: Scheduler
    ):
        self.scheduler_async = scheduler_async
        self.scheduler_sync = scheduler_sync

    async def solve_async_task(
            self,
            task: Callable[[...], Any],
            id_: str | None = None,
            run_date: datetime = None,
            *args,
            **kwargs
    ):
        trigger = DateTrigger(run_time=run_date) if run_date else None
        if trigger:
            await self.scheduler_async.add_schedule(
                func_or_task_id=task,
                trigger=trigger,
                id=id_,
                args=args,
                kwargs=kwargs
            )
        else:
            await self.scheduler_async.add_job(
                func_or_task_id=task,
                args=args,
                kwargs=kwargs
            )
        if self.scheduler_async.state == RunState.stopped:
            await self.scheduler_async.start_in_background()

    def solve_sync_task(
            self,
            task: Callable[[...], Any],
            id_: str | None = None,
            run_date: datetime = None,
            *args,
            **kwargs
    ):
        trigger = DateTrigger(run_time=run_date) if run_date else None
        if trigger:
            self.scheduler_sync.add_schedule(
                func_or_task_id=task,
                trigger=trigger,
                id=id_,
                args=args,
                kwargs=kwargs
            )
        else:
            self.scheduler_sync.add_job(
                func_or_task_id=task,
                args=args,
                kwargs=kwargs
            )
        if self.scheduler_sync.state == RunState.stopped:
            self.scheduler_sync.start_in_background()
