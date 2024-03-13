"""This is the base interface of interactor"""


class Interactor[InputDTO, OutputDTO]:
    async def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError
