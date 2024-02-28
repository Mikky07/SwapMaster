from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler

from swapmaster.application.common.task_solver import TaskSolver


class TaskSolverImp(TaskSolver):
    def __init__(self, scheduler: BackgroundScheduler):
        self.scheduler = scheduler

    def solve_task(self, task: Callable, *args, **kwargs):
        self.scheduler.add_job(task, args=args, kwargs=kwargs)
