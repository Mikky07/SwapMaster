from swapmaster.application.common import Notifier
from swapmaster.core.models import User


class TGBotNotifier(Notifier):
    def notify(self, user: User, notification: str, subject: str) -> None:
        ...
