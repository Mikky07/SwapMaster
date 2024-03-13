from swapmaster.application.common.uow import UoW


class UoWMock(UoW):
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    async def commit(self) -> None:
        if self.committed:
            raise ValueError("Cannot commit after rollback!")
        self.committed = True

    async def rollback(self) -> None:
        if self.committed:
            raise ValueError("Cannot rollback after commit!")
        self.rolled_back = True
