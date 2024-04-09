from dishka import Provider, from_context, provide, Scope

from swapmaster.adapters.db.gateways.sqlalchemy import UserGateway
from swapmaster.core.models import User


class TGUserProvider(Provider):
    scope = Scope.REQUEST

    user_gateway = from_context(provides=UserGateway)

    @provide
    async def get_user(self) -> User:
        ...

