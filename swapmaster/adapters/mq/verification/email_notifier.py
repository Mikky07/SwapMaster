import logging
from smtplib import SMTP_SSL

from swapmaster.adapters.mq.verification.config import EmailConfig
from swapmaster.application.common import Notifier
from swapmaster.application.common.task_solver import TaskSolver
from swapmaster.core.models import User


logger = logging.getLogger(__name__)
# need to optimize sending email


class EmailNotifier(Notifier):
    def __init__(self, config: EmailConfig, task_solver: TaskSolver):
        self.config = config
        self.task_solver = task_solver

    def send_email(self, username: str, email_address: str, text: str):
        message = \
            f"From: Swapmaster <{self.config.sender_email}>\r\n" \
            f"To: {username} <{email_address}>\r\n" \
            f"Subject: Swapmaster account confirmation\r\n\r\n"
        message += text
        server = SMTP_SSL(host=self.config.mail_server, port=self.config.port)
        server.login(self.config.sender_login, self.config.sender_password)
        server.sendmail(
            from_addr=self.config.sender_email,
            to_addrs=email_address,
            msg=message
        )
        server.quit()

    def notify(self, user: User, notification: str) -> None:
        self.task_solver.solve_task(
            self.send_email,
            username=user.username,
            email_address=user.email,
            text=notification
        )
