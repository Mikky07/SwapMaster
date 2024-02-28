from dataclasses import dataclass


@dataclass
class EmailConfig:
    mail_server: str
    port: int
    sender_login: str
    sender_password: str
    sender_email: str
