from datetime import datetime
from typing import Dict

from swapmaster.application.common.task_manager import AsyncTaskManager, TaskId, T_Task


class AsyncTaskManagerMock(AsyncTaskManager):
    def __init__(self):
        self.tasks_planned: Dict[TaskId, T_Task] = {}
        self.tasks_instantly_solved: list[int] = []

    async def solve_task(
            self,
            task: T_Task,
            *args,
            **kwargs
    ) -> None:
        self.tasks_instantly_solved.append(id(task))

    async def plan_task(
        self,
        task: T_Task,
        task_id: TaskId,
        run_date: datetime,
        *args,
        **kwargs
    ) -> TaskId:
        self.tasks_planned[task_id] = task
        return task_id

    async def get_planned_task(self, task_id: TaskId) -> T_Task:
        return self.tasks_planned[task_id]

    async def remove_planned_task(self, task_id: TaskId) -> None:
        del self.tasks_planned[task_id]
