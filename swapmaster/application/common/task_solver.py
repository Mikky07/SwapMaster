from datetime import datetime
from typing import Protocol
from abc import abstractmethod


class TaskSolver(Protocol):
    @abstractmethod
    def solve_task(self, task, id_, run_date: datetime = None, *args, **kwargs):
        raise NotImplementedError
