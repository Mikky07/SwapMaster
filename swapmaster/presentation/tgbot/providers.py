from aiogram.types import TelegramObject, Message, CallbackQuery
from dishka import Provider, from_context, provide, Scope

from swapmaster.adapters.mq.notification.bot_notifier import TGBotNotifier
from swapmaster.application import CreateUser
from swapmaster.application.common import UoW, Notifier
from swapmaster.application.common.gateways import UserReader, UserWriter
from swapmaster.application.common.verifier import Verifier
from swapmaster.application.user.create_user import NewUserDTO, attach_tg_id
from swapmaster.core.models import User
from swapmaster.presentation.tgbot.verifier import TGBotVerifier


class TGUserProvider(Provider):
    scope = Scope.REQUEST

    user_gateway = from_context(provides=UserReader)
    event = from_context(provides=TelegramObject)

    @provide
    async def get_user(
            self,
            uow: UoW,
            user_gateway: UserReader | UserWriter,
            event: TelegramObject,
            user_creator: CreateUser
    ) -> User:
        if type(event) in [Message, CallbackQuery]:
            user = await user_gateway.get_user_by_tg_id(tg_id=event.from_user.id)
            if not user:
                user = await user_creator(
                        data=NewUserDTO(
                            email=None,
                            password=None,
                            username=event.from_user.username
                        )
                    )
                await attach_tg_id(
                    user_id=user.id,
                    tg_id=event.from_user.id,
                    uow=uow,
                    user_gateway=user_gateway
                )
            return user


class TGBotNotifierProvider(Provider):
    scope = Scope.REQUEST

    bot_notifier = provide(source=TGBotNotifier, provides=Notifier)


class TGBotVerifierProvider(Provider):
    scope = Scope.REQUEST

    verifier = provide(source=TGBotVerifier, provides=Verifier)
