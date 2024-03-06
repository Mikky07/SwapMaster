from datetime import datetime
from typing import Protocol, Callable, Any, Coroutine
from abc import abstractmethod


class TaskSolver(Protocol):
    @abstractmethod
    async def solve_async_task(
            self,
            task: Callable[[...], Any],
            id_: str | None = None,
            run_date: datetime = None,
            *args,
            **kwargs
    ):
        raise NotImplementedError

    @abstractmethod
    def solve_sync_task(
            self,
            task: Callable[[...], Any],
            id_: str | None = None,
            run_date: datetime = None,
            *args,
            **kwargs
    ):
        raise NotImplementedError
