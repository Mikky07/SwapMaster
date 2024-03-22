"""Implementations of TaskManager ABC using APScheduler"""
from datetime import datetime
from typing import Callable, Coroutine, Any

from apscheduler import AsyncScheduler, Scheduler
from apscheduler.triggers.date import DateTrigger

from swapmaster.application.common.task_manager import TaskManager, TaskId, T_Task


class AsyncTaskManager(TaskManager[Coroutine[Any, Any, None]]):
    def __init__(
            self,
            scheduler: AsyncScheduler
    ):
        self.scheduler = scheduler

    async def solve_task(
            self,
            task: T_Task,
            *args,
            **kwargs
    ) -> None:
        await self.scheduler.add_job(
            func_or_task_id=task,
            args=args,
            kwargs=kwargs
        )

    async def plan_task(
        self,
        task: T_Task,
        task_id: TaskId,
        run_date: datetime,
        *args,
        **kwargs
    ) -> TaskId:
        trigger = DateTrigger(run_time=run_date)

        scheduled_task_id = await self.scheduler.add_schedule(
            func_or_task_id=task,
            trigger=trigger,
            id=task_id,
            args=args,
            kwargs=kwargs
        )

        return scheduled_task_id

    async def get_planned_task(self, task_id: TaskId) -> T_Task:
        ...

    async def remove_planned_task(self, task_id: TaskId) -> None:
        await self.scheduler.remove_schedule(
            id=task_id
        )


class SyncTaskManager(TaskManager[Callable[..., None]]):
    def __init__(
            self,
            scheduler: Scheduler
    ):
        self.scheduler = scheduler

    def solve_task(
            self,
            task: T_Task,
            *args,
            **kwargs
    ) -> None:
        self.scheduler.add_job(
            func_or_task_id=task,
            args=args,
            kwargs=kwargs
        )

    def plan_task(
        self,
        task: T_Task,
        task_id: TaskId,
        run_date: datetime,
        *args,
        **kwargs
    ) -> TaskId:
        trigger = DateTrigger(run_time=run_date)

        scheduled_task_id = self.scheduler.add_schedule(
            func_or_task_id=task,
            trigger=trigger,
            id=task_id,
            args=args,
            kwargs=kwargs
        )

        return scheduled_task_id

    def get_planned_task(self, task_id: TaskId) -> T_Task:
        ...

    def remove_planned_task(self, task_id: TaskId) -> None:
        ...
