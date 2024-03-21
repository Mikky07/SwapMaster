from swapmaster.application.common.notifier import Notifier
from swapmaster.core.models import User


class NotifierMock(Notifier):
    def __init__(self):
        self.notified = False

    def notify(self, user: User, notification: str, subject: str) -> None:
        self.notified = True
