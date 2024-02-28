from swapmaster.application.common import Notifier
from swapmaster.core.models import User


# this app using only one class for verification

class Verifier:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def notify_user(self, user: User):
        verification_link = self.__create_verification_link()
        verification_text = self.__create_notification(user=user, link=verification_link)
        self.notifier.notify(user=user, notification=verification_text)

    def __create_notification(self, user: User, link: str):
        verification_text = (
            "Welcome, {username}!\n"
            "Follow the link to verify your account: "
        ).format(username=user.username) + link
        return verification_text

    #stub
    def __create_verification_link(self) -> str:
        return "https://www.google.com/"
