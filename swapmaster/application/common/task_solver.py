from typing import Protocol, Callable
from abc import abstractmethod


class TaskSolver(Protocol):
    @abstractmethod
    def solve_task(self, task: Callable, *args, **kwargs):
        raise NotImplementedError
