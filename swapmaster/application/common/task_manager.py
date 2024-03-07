from datetime import datetime
from typing import Protocol, Callable, Any
from abc import abstractmethod


class TaskManager(Protocol):
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

    @abstractmethod
    def remove_sync_task(self, task_id: str):
        raise NotImplementedError

    @abstractmethod
    async def remove_async_task(self, task_id: str):
        raise NotImplementedError
