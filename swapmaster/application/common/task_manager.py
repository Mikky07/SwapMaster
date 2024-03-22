from datetime import datetime
from typing import TypeAlias, Generic, TypeVar, Coroutine, Any
from abc import abstractmethod, ABC

TaskId: TypeAlias = str
T_Task = TypeVar("T_Task")


class BaseTaskManager(Generic[T_Task]):
    @abstractmethod
    def plan_task(
        self,
        task: T_Task,
        task_id: TaskId,
        run_date: datetime,
        *args,
        **kwargs
    ) -> TaskId:
        raise NotImplementedError

    @abstractmethod
    def solve_task(
            self,
            task: T_Task,
            *args,
            **kwargs
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_planned_task(self, task_id: TaskId) -> T_Task:
        raise NotImplementedError

    @abstractmethod
    def remove_planned_task(self, task_id: TaskId) -> None:
        raise NotImplementedError


class AsyncTaskManager(ABC, BaseTaskManager[Coroutine[Any, Any, None]]):
    @abstractmethod
    async def solve_task(
            self,
            task: T_Task,
            *args,
            **kwargs
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def plan_task(
        self,
        task: T_Task,
        task_id: TaskId,
        run_date: datetime,
        *args,
        **kwargs
    ) -> TaskId:
        raise NotImplementedError

    @abstractmethod
    async def remove_planned_task(self, task_id: TaskId) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_planned_task(self, task_id: TaskId) -> T_Task:
        raise NotImplementedError
