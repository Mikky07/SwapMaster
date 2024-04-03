from typing import Callable, Dict, Any, Awaitable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject

from swapmaster.presentation.interactor_factory import InteractorFactory


class IoCMiddleware(BaseMiddleware):
    def __init__(self, ioc: InteractorFactory):
        self.ioc = ioc

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data['ioc'] = self.ioc
        await handler(event, data)
