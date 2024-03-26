from abc import abstractmethod
from typing import AsyncContextManager

from swapmaster.application import WebVerifier
from swapmaster.presentation.interactor_factory import InteractorFactory


class WebInteractorFactory(InteractorFactory):
    @abstractmethod
    async def get_web_verifier(self) -> AsyncContextManager[WebVerifier]:
        raise NotImplementedError
