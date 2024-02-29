import logging
from smtplib import SMTP_SSL

from dns.resolver import resolve, NXDOMAIN

from swapmaster.adapters.mq.notification.config import EmailConfig
from swapmaster.application.common import Notifier
from swapmaster.application.common.task_solver import TaskSolver
from swapmaster.core.models import User
from swapmaster.core.utils.exceptions import SMError

logger = logging.getLogger(__name__)


class EmailNotifier(Notifier):
    def __init__(self, config: EmailConfig, task_solver: TaskSolver):
        self.config = config
        self.task_solver = task_solver

    def is_mx_available(self, mx: str):
        try:
            resolve(mx, "MX", raise_on_no_answer=False)
        except NXDOMAIN:
            raise SMError("MX: {mx} is not available!".format(mx=mx))

    def create_message(self, username: str, email_address: str, text: str, subject: str) -> str:
        message = \
            f"From: Swapmaster <{self.config.sender_email}>\r\n" \
            f"To: {username} <{email_address}>\r\n" \
            f"Subject: {subject}\r\n\r\n"
        message += text
        return message

    def send_email(self, username: str, email_address: str, text: str, subject: str):
        mx = email_address.split("@")[-1]
        self.is_mx_available(mx)

        message = self.create_message(username, email_address, text, subject)

        server = SMTP_SSL(host=self.config.mail_server, port=self.config.port)
        server.login(self.config.sender_login, self.config.sender_password)
        server.sendmail(
            from_addr=self.config.sender_email,
            to_addrs=email_address,
            msg=message
        )
        server.quit()

    def notify(self, user: User, notification: str, subject: str) -> None:
        self.task_solver.solve_task(
            self.send_email,
            username=user.username,
            email_address=user.email,
            text=notification,
            subject=subject
        )
