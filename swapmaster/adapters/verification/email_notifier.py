import logging

from swapmaster.application.common import Notifier
from swapmaster.core.models import User


logger = logging.getLogger(__name__)


class EmailNotifier(Notifier):
    def __init__(self):
        ...

    async def notify(self, user: User, notification: str) -> None:
        logger.debug("Notification wanna be sent")
