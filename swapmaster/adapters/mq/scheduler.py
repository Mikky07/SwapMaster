from datetime import datetime
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from swapmaster.application.common.task_solver import TaskSolver


class TaskSolverImp(TaskSolver):
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler

    def solve_task(self, task, id_=None, run_date: datetime = None, *args, **kwargs):
        trigger = DateTrigger(run_date=run_date) if run_date else None
        self.scheduler.add_job(task, id=id_, trigger=trigger, args=args, kwargs=kwargs)
