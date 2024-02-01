from typing import TypeVar, Callable, Generic

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")

# get from https://github.com/Tishka17/deseos17/blob/master/src/deseos17/application/common/interactor.py


class Interactor(Generic[InputDTO, OutputDTO]):
    async def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError


InteractorT = TypeVar("InteractorT", bound=Interactor)
InteractorFactory = Callable[[], InteractorT]
